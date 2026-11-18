import hashlib
import hmac
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, Product, CartItem, Order, Payment

app = create_app()

def test_payments():
    print("======================================================================")
    print("💳 KARTHIK'S CART PAYMENT GATEWAY VERIFICATION")
    print("======================================================================")

    client = app.test_client()
    test_email = os.getenv('TEST_CUSTOMER_EMAIL') or os.getenv('SEED_CUSTOMER_EMAIL')
    test_password = os.getenv('TEST_CUSTOMER_PASSWORD') or os.getenv('SEED_CUSTOMER_PASSWORD')
    if not test_email or not test_password:
        raise RuntimeError('Set TEST_CUSTOMER_EMAIL and TEST_CUSTOMER_PASSWORD before running payment tests.')

    with app.app_context():
        # Authenticate customer
        login_res = client.post('/api/auth/login', json={
            'email': test_email,
            'password': test_password
        })
        assert login_res.status_code == 200, f"Login failed: {login_res.data}"
        token = login_res.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        print("  ✓ Authenticated test customer")

        # Pick an in-stock product
        product = Product.query.filter(Product.stock >= 5).first()
        initial_stock = product.stock
        print(f"  ✓ Selected Product: '{product.name}' (Stock: {initial_stock}, Price: ₹{product.discounted_price})")

        # Add to cart
        client.post('/api/cart/clear', headers=headers)
        add_res = client.post('/api/cart', headers=headers, json={
            'product_id': product.id,
            'quantity': 2,
            'size': 'M',
            'color': 'Black'
        })
        assert add_res.status_code == 200
        print("  ✓ Added 2 units to shopping cart.")

        # Test 1: Place Online Razorpay Order
        print("\n[TEST 1] Create Online Payment Order via /api/orders")
        order_res = client.post('/api/orders', headers=headers, json={
            'shipping_address': {
                'full_name': 'Karthik S',
                'mobile_number': '9876543210',
                'address_line1': '123 Tech Park Road',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'postal_code': '560001'
            },
            'payment_method': 'razorpay',
            'coupon_code': 'SHOPORA10'
        })
        assert order_res.status_code in (200, 201), f"Create order failed: {order_res.data}"
        order_data = order_res.get_json()
        order = order_data['order']
        razorpay_info = order_data['razorpay']
        assert order['payment_status'] == 'pending'
        assert razorpay_info['name'] == "Karthik's Cart"
        assert razorpay_info['amount_paise'] > 0
        print(f"  ✓ Order #{order['order_number']} created. Total: ₹{order['total_amount']} (Status: {order['payment_status']})")
        print(f"  ✓ Razorpay Order ID generated: {razorpay_info['order_id']}")

        # Test 2: Cryptographic Payment Verification & Stock Deduction
        print("\n[TEST 2] Complete Cryptographic Payment Verification via /api/payments/verify")
        payment_id = f"pay_test_{order['id']}_123"
        signature = hmac.new(
            app.config['RAZORPAY_KEY_SECRET'].encode('utf-8'),
            f"{razorpay_info['order_id']}|{payment_id}".encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()
        verify_res = client.post('/api/payments/verify', headers=headers, json={
            'order_id': order['id'],
            'razorpay_order_id': razorpay_info['order_id'],
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        assert verify_res.status_code == 200, f"Verification failed: {verify_res.data}"
        verified_order = verify_res.get_json()['order']
        assert verified_order['payment_status'] == 'paid'
        assert verified_order['order_status'] == 'confirmed'
        print(f"  ✓ Payment verified! Order status updated to: {verified_order['payment_status']} / {verified_order['order_status']}")

        # Verify stock was safely decremented in PostgreSQL
        product_after = Product.query.get(product.id)
        assert product_after.stock == initial_stock - 2, f"Stock mismatch! Expected {initial_stock - 2}, got {product_after.stock}"
        print(f"  ✓ Product stock safely decremented from {initial_stock} to {product_after.stock} in PostgreSQL.")

        # Verify cart was cleared
        cart_res = client.get('/api/cart', headers=headers)
        assert len(cart_res.get_json()['cart']['items']) == 0
        print("  ✓ Shopping cart cleared automatically post-payment.")

        # Test 3: Cash on Delivery (COD) Flow
        print("\n[TEST 3] Cash on Delivery (COD) Checkout Flow")
        # Add 1 unit
        client.post('/api/cart', headers=headers, json={
            'product_id': product.id,
            'quantity': 1
        })
        cod_res = client.post('/api/orders', headers=headers, json={
            'shipping_address': {
                'full_name': 'Karthik S',
                'mobile_number': '9876543210',
                'address_line1': '123 Tech Park Road',
                'city': 'Bengaluru',
                'state': 'Karnataka',
                'postal_code': '560001'
            },
            'payment_method': 'cod'
        })
        assert cod_res.status_code in (200, 201), f"COD failed: {cod_res.data}"
        cod_order = cod_res.get_json()['order']
        assert cod_order['payment_method'] == 'cod'
        assert cod_order['order_status'] == 'confirmed'
        print(f"  ✓ COD Order #{cod_order['order_number']} confirmed immediately.")

        # Restore product stock for clean database state
        product_after.stock = initial_stock
        db.session.commit()
        print("  ✓ Database stock restored cleanly.")

    print("\n======================================================================")
    print("🎉 ALL PAYMENT GATEWAY TESTS PASSED SUCCESSFULLY!")
    print("======================================================================")
    return True

if __name__ == '__main__':
    success = test_payments()
    if not success:
        sys.exit(1)
