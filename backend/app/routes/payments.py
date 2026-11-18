from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import db, Order, Payment, Product, CartItem
from app.services.razorpay_service import RazorpayService
from app.utils.auth_decorators import customer_required

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/create-order', methods=['POST'])
@customer_required()
def create_payment_order():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    order_id = data.get('order_id')

    if not order_id:
        return jsonify({'success': False, 'message': 'order_id is required'}), 400

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'success': False, 'message': 'Order not found'}), 404

    if order.payment_status == 'paid':
        return jsonify({'success': False, 'message': 'Order is already paid'}), 400

    # Create or retrieve Razorpay payment order
    rzp_order = RazorpayService.create_order(
        amount=order.total_amount,
        receipt_id=order.order_number,
        currency='INR',
        notes={'order_id': order.id, 'user_id': user_id}
    )

    order.razorpay_order_id = rzp_order['id']
    db.session.commit()

    return jsonify({
        'success': True,
        'razorpay_order': rzp_order
    }), 200

@payments_bp.route('/verify', methods=['POST'])
@customer_required()
def verify_payment():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    order_id = data.get('order_id')
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')

    if not all([order_id, razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        return jsonify({'success': False, 'message': 'Incomplete payment verification payload'}), 400

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'success': False, 'message': 'Order not found'}), 404

    if order.payment_status == 'paid':
        return jsonify({
            'success': True,
            'message': 'Payment already verified',
            'order': order.to_dict()
        }), 200

    # Backend cryptographic verification of Razorpay HMAC-SHA256 signature
    is_valid = RazorpayService.verify_payment_signature(
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_signature=razorpay_signature
    )

    if not is_valid:
        # Record failed payment record
        failed_pay = Payment(
            order_id=order.id,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            amount=order.total_amount,
            status='failed',
            method='razorpay',
            error_code='SIGNATURE_MISMATCH',
            error_description='Invalid Razorpay cryptographic signature'
        )
        db.session.add(failed_pay)
        order.payment_status = 'failed'
        db.session.commit()

        return jsonify({'success': False, 'message': 'Payment verification failed: invalid signature'}), 400

    # Safe stock deduction upon confirmed payment verification
    try:
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock = max(0, product.stock - item.quantity)

        # Update Order
        order.payment_status = 'paid'
        order.order_status = 'confirmed'
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_order_id = razorpay_order_id

        # Record verified Payment record
        payment = Payment(
            order_id=order.id,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            amount=order.total_amount,
            currency='INR',
            status='captured',
            method='razorpay'
        )
        db.session.add(payment)

        # Clear cart for user
        CartItem.query.filter_by(user_id=user_id).delete()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error completing order payment', 'error': str(e)}), 500

@payments_bp.route('/<int:id>', methods=['GET'])
@customer_required()
def get_payment_details(id):
    payment = Payment.query.get(id)
    if not payment:
        return jsonify({'success': False, 'message': 'Payment record not found'}), 404
    return jsonify({'success': True, 'payment': payment.to_dict()}), 200
