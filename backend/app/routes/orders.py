from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import db, Order, OrderItem, Product, CartItem, Coupon, Payment
from app.services.razorpay_service import RazorpayService
from app.utils.auth_decorators import customer_required
from flask import current_app

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['POST'])
@customer_required()
def create_order():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    shipping = data.get('shipping_address') or {}
    shipping_name = shipping.get('full_name', '').strip()
    shipping_mobile = shipping.get('mobile_number', '').strip()
    shipping_address_text = shipping.get('address_line1', '').strip()
    if shipping.get('address_line2'):
        shipping_address_text += f", {shipping.get('address_line2').strip()}"
    shipping_city = shipping.get('city', '').strip()
    shipping_state = shipping.get('state', '').strip()
    shipping_postal_code = shipping.get('postal_code', '').strip()

    payment_method = data.get('payment_method', 'razorpay').lower()
    coupon_code = data.get('coupon_code', '').strip().upper()

    if not all([shipping_name, shipping_mobile, shipping_address_text, shipping_city, shipping_state, shipping_postal_code]):
        return jsonify({'success': False, 'message': 'Complete shipping address is required'}), 400

    if payment_method not in ('razorpay', 'cod'):
        return jsonify({'success': False, 'message': 'Invalid payment method'}), 400

    # Get items: either direct buy item or from cart
    buy_now_item = data.get('buy_now_item')
    order_items_data = []

    if buy_now_item:
        p_id = buy_now_item.get('product_id')
        qty = int(buy_now_item.get('quantity', 1))
        product = Product.query.get(p_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        if product.stock < qty:
            return jsonify({'success': False, 'message': f'Insufficient stock for {product.name}'}), 400

        order_items_data.append({
            'product': product,
            'quantity': qty,
            'size': buy_now_item.get('size'),
            'color': buy_now_item.get('color'),
            'price': float(product.discounted_price)
        })
    else:
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({'success': False, 'message': 'Your cart is empty'}), 400

        for ci in cart_items:
            if not ci.product:
                continue
            if ci.product.stock < ci.quantity:
                return jsonify({'success': False, 'message': f"Insufficient stock for '{ci.product.name}'. Only {ci.product.stock} available."}), 400

            unit_price = float(ci.product.discounted_price)
            if ci.variant and ci.variant.additional_price:
                unit_price += float(ci.variant.additional_price)

            order_items_data.append({
                'product': ci.product,
                'quantity': ci.quantity,
                'size': ci.size,
                'color': ci.color,
                'price': unit_price
            })

    if not order_items_data:
        return jsonify({'success': False, 'message': 'No items to order'}), 400

    # Calculate financial totals
    subtotal = sum(item['price'] * item['quantity'] for item in order_items_data)
    delivery_charge = 0.0 if (subtotal >= 999.0 or subtotal == 0.0) else 99.0

    discount = 0.0
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
        if coupon:
            discount = coupon.calculate_discount(subtotal)

    total_amount = max(0.0, round(subtotal - discount + delivery_charge, 2))

    try:
        order = Order(
            order_number=Order.generate_order_number(),
            user_id=user_id,
            shipping_name=shipping_name,
            shipping_mobile=shipping_mobile,
            shipping_address_text=shipping_address_text,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_postal_code=shipping_postal_code,
            subtotal=round(subtotal, 2),
            discount=round(discount, 2),
            delivery_charge=round(delivery_charge, 2),
            total_amount=total_amount,
            payment_method=payment_method,
            payment_status='pending',
            order_status='placed'
        )
        db.session.add(order)
        db.session.flush()

        for itm in order_items_data:
            p = itm['product']
            oi = OrderItem(
                order_id=order.id,
                product_id=p.id,
                product_name=p.name,
                product_image=p.images[0].image_url if p.images else None,
                price=itm['price'],
                quantity=itm['quantity'],
                size=itm['size'],
                color=itm['color'],
                total_price=round(itm['price'] * itm['quantity'], 2)
            )
            db.session.add(oi)

            # If COD, decrement stock immediately and clear cart
            if payment_method == 'cod':
                p.stock = max(0, p.stock - itm['quantity'])

        if payment_method == 'cod':
            order.order_status = 'confirmed'
            # Clear cart if from cart
            if not buy_now_item:
                CartItem.query.filter_by(user_id=user_id).delete()

            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Order placed successfully with Cash on Delivery',
                'order': order.to_dict()
            }), 201

        # Online Razorpay payment
        razorpay_order = RazorpayService.create_order(
            amount=total_amount,
            receipt_id=order.order_number,
            currency='INR',
            notes={'order_id': order.id, 'user_id': user_id}
        )

        order.razorpay_order_id = razorpay_order['id']
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order initialized for payment',
            'order': order.to_dict(),
            'razorpay': {
                'key_id': current_app.config.get('RAZORPAY_KEY_ID'),
                'order_id': razorpay_order['id'],
                'amount_paise': razorpay_order['amount_paise'],
                'amount': total_amount,
                'currency': 'INR',
                'name': "Karthik's Cart",
                'description': f"Payment for Order #{order.order_number}",
                'prefill': {
                    'name': shipping_name,
                    'contact': shipping_mobile
                }
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to create order', 'error': str(e)}), 500

@orders_bp.route('', methods=['GET'])
@customer_required()
def get_user_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify({
        'success': True,
        'orders': [o.to_dict() for o in orders]
    }), 200

@orders_bp.route('/<int:id>', methods=['GET'])
@customer_required()
def get_order_details(id):
    user_id = int(get_jwt_identity())
    order = Order.query.get(id)
    if not order:
        return jsonify({'success': False, 'message': 'Order not found'}), 404

    from app.models.user import User
    user = User.query.get(user_id)
    if order.user_id != user_id and (not user or user.role != 'admin'):
        return jsonify({'success': False, 'message': 'Unauthorized to view this order'}), 403

    return jsonify({'success': True, 'order': order.to_dict()}), 200

@orders_bp.route('/<int:id>/cancel', methods=['PUT'])
@customer_required()
def cancel_order(id):
    user_id = int(get_jwt_identity())
    order = Order.query.get(id)
    if not order:
        return jsonify({'success': False, 'message': 'Order not found'}), 404

    from app.models.user import User
    user = User.query.get(user_id)
    if order.user_id != user_id and (not user or user.role != 'admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    if order.order_status in ('delivered', 'cancelled'):
        return jsonify({'success': False, 'message': f'Order cannot be cancelled as it is already {order.order_status}'}), 400

    # Restore inventory for each item if stock was already decremented (paid or cod)
    if order.payment_status == 'paid' or order.payment_method == 'cod':
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity

    order.order_status = 'cancelled'
    if order.payment_status == 'paid':
        order.payment_status = 'refunded'

    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Order has been successfully cancelled',
        'order': order.to_dict()
    }), 200
