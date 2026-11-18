from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import db, CartItem, Product, ProductVariant, Coupon, Wishlist
from app.utils.auth_decorators import customer_required

cart_bp = Blueprint('cart', __name__)

def calculate_cart_totals(user_id, coupon_code=None):
    items = CartItem.query.filter_by(user_id=user_id).order_by(CartItem.created_at.desc()).all()
    subtotal = 0.0
    items_count = 0
    has_out_of_stock = False
    has_exceeded_stock = False

    serialized_items = []
    for item in items:
        item_dict = item.to_dict()
        subtotal += item_dict['total_price']
        items_count += item.quantity
        if item_dict['is_out_of_stock']:
            has_out_of_stock = True
        if item_dict['exceeds_stock']:
            has_exceeded_stock = True
        serialized_items.append(item_dict)

    # Free delivery over 999 INR, otherwise 99 INR delivery fee (0 if cart is empty)
    delivery_charge = 0.0 if (subtotal >= 999.0 or subtotal == 0.0) else 99.0

    discount = 0.0
    applied_coupon = None
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code.strip().upper(), is_active=True).first()
        if coupon:
            discount = coupon.calculate_discount(subtotal)
            applied_coupon = coupon.to_dict()

    final_total = max(0.0, subtotal - discount + delivery_charge)
    can_checkout = (len(items) > 0) and (not has_out_of_stock) and (not has_exceeded_stock)

    return {
        'items': serialized_items,
        'items_count': items_count,
        'subtotal': round(subtotal, 2),
        'discount': round(discount, 2),
        'delivery_charge': round(delivery_charge, 2),
        'final_total': round(final_total, 2),
        'has_out_of_stock': has_out_of_stock,
        'has_exceeded_stock': has_exceeded_stock,
        'can_checkout': can_checkout,
        'applied_coupon': applied_coupon
    }

@cart_bp.route('', methods=['GET'])
@customer_required()
def get_cart():
    user_id = int(get_jwt_identity())
    coupon_code = request.args.get('coupon', '')
    summary = calculate_cart_totals(user_id, coupon_code)
    return jsonify({'success': True, 'cart': summary}), 200

@cart_bp.route('', methods=['POST'])
@customer_required()
def add_to_cart():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    product_id = data.get('product_id')
    size = data.get('size')
    color = data.get('color')
    
    try:
        quantity = int(data.get('quantity', 1))
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Quantity must be a valid integer'}), 400

    if not product_id or quantity <= 0:
        return jsonify({'success': False, 'message': 'Invalid product or quantity'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    # Strict backend stock check (never trust frontend prices or stock)
    if product.stock <= 0:
        return jsonify({'success': False, 'message': f"'{product.name}' is currently out of stock"}), 400

    if quantity > product.stock:
        return jsonify({'success': False, 'message': f"Cannot add {quantity} units. Only {product.stock} items left in stock."}), 400

    # Check for existing item with identical product_id, size, and color
    existing_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id,
        size=size,
        color=color
    ).first()

    if existing_item:
        new_qty = existing_item.quantity + quantity
        if new_qty > product.stock:
            return jsonify({
                'success': False,
                'message': f"Cannot add {quantity} more. You already have {existing_item.quantity} in your cart, and only {product.stock} are available."
            }), 400
        existing_item.quantity = new_qty
    else:
        # Match variant if available
        variant = None
        if size or color:
            query = ProductVariant.query.filter_by(product_id=product_id)
            if size:
                query = query.filter_by(size=size)
            if color:
                query = query.filter_by(color=color)
            variant = query.first()

        new_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            variant_id=variant.id if variant else None,
            size=size,
            color=color,
            quantity=quantity
        )
        db.session.add(new_item)

    db.session.commit()
    summary = calculate_cart_totals(user_id)
    return jsonify({
        'success': True,
        'message': f"Added '{product.name}' to cart",
        'cart': summary
    }), 200

@cart_bp.route('/<int:id>', methods=['PUT'])
@customer_required()
def update_cart_item(id):
    user_id = int(get_jwt_identity())
    item = CartItem.query.filter_by(id=id, user_id=user_id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Cart item not found'}), 404

    data = request.get_json() or {}
    
    # Handle size or color variant change if passed
    size_changed = 'size' in data and data['size'] != item.size
    color_changed = 'color' in data and data['color'] != item.color

    if size_changed or color_changed:
        new_size = data.get('size', item.size)
        new_color = data.get('color', item.color)

        # Check if another cart item exists with target size & color
        other_item = CartItem.query.filter(
            CartItem.user_id == user_id,
            CartItem.product_id == item.product_id,
            CartItem.size == new_size,
            CartItem.color == new_color,
            CartItem.id != item.id
        ).first()

        if other_item:
            # Merge into other item
            merged_qty = other_item.quantity + item.quantity
            stock = item.product.stock if item.product else 0
            if merged_qty > stock:
                return jsonify({'success': False, 'message': f'Cannot merge variant. Total exceeds available stock of {stock}.'}), 400
            other_item.quantity = merged_qty
            db.session.delete(item)
            db.session.commit()
            summary = calculate_cart_totals(user_id)
            return jsonify({'success': True, 'message': 'Variants merged successfully', 'cart': summary}), 200
        else:
            item.size = new_size
            item.color = new_color

    # Handle quantity update
    if 'quantity' in data:
        try:
            quantity = int(data['quantity'])
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Quantity must be a valid integer'}), 400

        if quantity <= 0:
            db.session.delete(item)
        else:
            if item.product and quantity > item.product.stock:
                return jsonify({
                    'success': False,
                    'message': f"Cannot select {quantity} units. Only {item.product.stock} items available in stock."
                }), 400
            item.quantity = quantity

    db.session.commit()
    summary = calculate_cart_totals(user_id)
    return jsonify({'success': True, 'message': 'Cart updated successfully', 'cart': summary}), 200

@cart_bp.route('/<int:id>', methods=['DELETE'])
@customer_required()
def remove_from_cart(id):
    user_id = int(get_jwt_identity())
    item = CartItem.query.filter_by(id=id, user_id=user_id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Cart item not found'}), 404

    prod_name = item.product.name if item.product else 'Item'
    db.session.delete(item)
    db.session.commit()
    summary = calculate_cart_totals(user_id)
    return jsonify({
        'success': True,
        'message': f"Removed '{prod_name}' from cart",
        'cart': summary
    }), 200

@cart_bp.route('/<int:id>/move-to-wishlist', methods=['POST'])
@customer_required()
def move_item_to_wishlist(id):
    user_id = int(get_jwt_identity())
    item = CartItem.query.filter_by(id=id, user_id=user_id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Cart item not found'}), 404

    product_id = item.product_id
    prod_name = item.product.name if item.product else 'Product'

    # Check if already in wishlist; if not, add it
    existing_wish = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not existing_wish:
        new_wish = Wishlist(user_id=user_id, product_id=product_id)
        db.session.add(new_wish)

    # Delete from cart
    db.session.delete(item)
    db.session.commit()

    summary = calculate_cart_totals(user_id)
    wishlist_count = Wishlist.query.filter_by(user_id=user_id).count()

    return jsonify({
        'success': True,
        'message': f"Moved '{prod_name}' to your wishlist",
        'cart': summary,
        'wishlist_count': wishlist_count
    }), 200

@cart_bp.route('/clear', methods=['POST'])
@customer_required()
def clear_cart():
    user_id = int(get_jwt_identity())
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    summary = calculate_cart_totals(user_id)
    return jsonify({'success': True, 'message': 'Cart cleared', 'cart': summary}), 200

@cart_bp.route('/apply-coupon', methods=['POST'])
@customer_required()
def apply_coupon():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    code = data.get('code', '').strip().upper()

    if not code:
        return jsonify({'success': False, 'message': 'Coupon code is required'}), 400

    coupon = Coupon.query.filter_by(code=code, is_active=True).first()
    if not coupon:
        return jsonify({'success': False, 'message': f"Coupon '{code}' is invalid or expired"}), 404

    summary = calculate_cart_totals(user_id, coupon_code=code)
    if summary['discount'] <= 0:
        return jsonify({
            'success': False,
            'message': f"Coupon requires a minimum order amount of ₹{coupon.min_order_amount:.0f}. Current subtotal: ₹{summary['subtotal']:.0f}."
        }), 400

    return jsonify({
        'success': True,
        'message': f"Coupon '{code}' applied! You saved ₹{summary['discount']:.2f}",
        'cart': summary
    }), 200
