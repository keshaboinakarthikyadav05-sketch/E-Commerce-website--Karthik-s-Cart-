import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, Product, CartItem, Wishlist, Coupon, ProductVariant

app = create_app()

def run_tests():
    print("======================================================================")
    print("🚀 KARTHIK's CART PHASE 6: SHOPPING CART & WISHLIST TEST SUITE")
    print("======================================================================")

    client = app.test_client()
    passed_tests = 0
    total_tests = 12
    test_email = os.getenv('TEST_CUSTOMER_EMAIL') or os.getenv('SEED_CUSTOMER_EMAIL')
    test_password = os.getenv('TEST_CUSTOMER_PASSWORD') or os.getenv('SEED_CUSTOMER_PASSWORD')
    if not test_email or not test_password:
        print("Test setup requires TEST_CUSTOMER_EMAIL and TEST_CUSTOMER_PASSWORD.")
        return False

    with app.app_context():
        # Ensure customer user exists
        user = User.query.filter_by(email=test_email).first()
        if not user:
            print(f"Test setup failed: {test_email} does not exist.")
            return False

        # Clean slate for test user
        CartItem.query.filter_by(user_id=user.id).delete()
        Wishlist.query.filter_by(user_id=user.id).delete()
        db.session.commit()

        # Step 1: Login & obtain JWT
        print("\n[TEST 1] Customer Authentication & JWT Session")
        login_res = client.post('/api/auth/login', json={
            'email': test_email,
            'password': test_password
        })
        assert login_res.status_code == 200, f"Login failed: {login_res.data}"
        token = login_res.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        print("  ✓ Customer authenticated successfully. Token received.")
        passed_tests += 1

        # Step 2: Empty Cart State
        print("\n[TEST 2] Initial Empty Cart State & Totals")
        cart_res = client.get('/api/cart', headers=headers)
        assert cart_res.status_code == 200
        cart_data = cart_res.get_json()['cart']
        assert cart_data['items'] == []
        assert cart_data['items_count'] == 0
        assert cart_data['subtotal'] == 0.0
        assert cart_data['delivery_charge'] == 0.0
        assert cart_data['final_total'] == 0.0
        assert cart_data['can_checkout'] is False
        print("  ✓ Empty cart returns zeroed totals and can_checkout=False.")
        passed_tests += 1

        # Pick an in-stock product with variants
        product = Product.query.filter(Product.stock > 10).first()
        assert product is not None, "No in-stock product found in database"
        print(f"  Using Product: ID {product.id} - '{product.name}' (Stock: {product.stock}, Price: ₹{product.discounted_price})")

        # Step 3: Add Product to Cart with Size & Color (Strict Backend Pricing)
        print("\n[TEST 3] Add Product to Cart with Variant (Backend Price Calculation)")
        add_res = client.post('/api/cart', headers=headers, json={
            'product_id': product.id,
            'quantity': 2,
            'size': 'M',
            'color': 'Black',
            'unit_price': 1.0  # Intentional tampered price to verify backend ignores it
        })
        assert add_res.status_code == 200
        cart_data = add_res.get_json()['cart']
        assert cart_data['items_count'] == 2
        item = cart_data['items'][0]
        # Verify backend enforced true database price
        assert item['unit_price'] == product.discounted_price, f"Price tampered! Expected {product.discounted_price}, got {item['unit_price']}"
        assert item['total_price'] == product.discounted_price * 2
        assert item['size'] == 'M'
        assert item['color'] == 'Black'
        assert item['is_out_of_stock'] is False
        print(f"  ✓ Added 2 units with variant (Size: M, Color: Black).")
        print(f"  ✓ Backend price integrity confirmed: enforced database price ₹{item['unit_price']} (ignored tampered ₹1.0).")
        passed_tests += 1

        cart_item_id = item['id']

        # Step 4: Update Quantity within Stock Limit
        print("\n[TEST 4] Update Quantity within Stock Limit")
        update_res = client.put(f'/api/cart/{cart_item_id}', headers=headers, json={
            'quantity': 3
        })
        assert update_res.status_code == 200
        cart_data = update_res.get_json()['cart']
        assert cart_data['items_count'] == 3
        assert cart_data['subtotal'] == product.discounted_price * 3
        print(f"  ✓ Updated quantity to 3. New Subtotal: ₹{cart_data['subtotal']}")
        passed_tests += 1

        # Step 5: Prevent Ordering Quantities Exceeding Available Stock
        print("\n[TEST 5] Prevent Quantities Exceeding Stock Limit")
        excess_qty = product.stock + 10
        exceed_res = client.put(f'/api/cart/{cart_item_id}', headers=headers, json={
            'quantity': excess_qty
        })
        assert exceed_res.status_code == 400
        err_msg = exceed_res.get_json()['message']
        print(f"  ✓ Excess quantity ({excess_qty}) rejected with message: '{err_msg}'")

        add_exceed = client.post('/api/cart', headers=headers, json={
            'product_id': product.id,
            'quantity': excess_qty
        })
        assert add_exceed.status_code == 400
        print(f"  ✓ Adding excess quantity rejected at entry.")
        passed_tests += 1

        # Step 6: Variant Selection & Merging in Cart
        print("\n[TEST 6] Select/Update Product Variants in Cart")
        variant_res = client.put(f'/api/cart/{cart_item_id}', headers=headers, json={
            'size': 'L',
            'color': 'Blue'
        })
        assert variant_res.status_code == 200
        cart_data = variant_res.get_json()['cart']
        assert cart_data['items'][0]['size'] == 'L'
        assert cart_data['items'][0]['color'] == 'Blue'
        print("  ✓ Product variant updated directly in cart to Size: L, Color: Blue.")
        passed_tests += 1

        # Step 7: Delivery Charge and Coupon Discount Calculation
        print("\n[TEST 7] Financial Calculations: Subtotal, Delivery Fee & Coupon Discount")
        # Ensure subtotal is enough to test coupons
        coupon_res = client.post('/api/cart/apply-coupon', headers=headers, json={
            'code': 'SHOPORA10'
        })
        assert coupon_res.status_code == 200, f"Coupon failed: {coupon_res.data}"
        cart_data = coupon_res.get_json()['cart']
        subtotal = cart_data['subtotal']
        expected_discount = round(subtotal * 0.10, 2)
        assert cart_data['discount'] == expected_discount
        expected_delivery = 0.0 if subtotal >= 999.0 else 99.0
        assert cart_data['delivery_charge'] == expected_delivery
        expected_final = round(subtotal - expected_discount + expected_delivery, 2)
        assert cart_data['final_total'] == expected_final
        print(f"  ✓ Subtotal: ₹{subtotal}")
        print(f"  ✓ Coupon discount (10%): -₹{cart_data['discount']}")
        print(f"  ✓ Delivery Charge: ₹{cart_data['delivery_charge']} ({'FREE over ₹999' if expected_delivery == 0 else 'Standard Delivery'})")
        print(f"  ✓ Final Total: ₹{cart_data['final_total']}")
        passed_tests += 1

        # Step 8: Out-of-Stock and Stock Limit Visibility
        print("\n[TEST 8] Out-of-Stock and Stock Limit Detection")
        original_stock = product.stock
        try:
            # Simulate out-of-stock scenario on the cart product
            product.stock = 0
            db.session.commit()

            cart_check = client.get('/api/cart', headers=headers)
            cart_data = cart_check.get_json()['cart']
            assert cart_data['has_out_of_stock'] is True
            assert cart_data['can_checkout'] is False
            assert cart_data['items'][0]['is_out_of_stock'] is True
            print("  ✓ Out-of-stock product successfully flagged.")
            print("  ✓ can_checkout safely turned to False.")

            # Attempt to add out-of-stock product
            add_out = client.post('/api/cart', headers=headers, json={
                'product_id': product.id,
                'quantity': 1
            })
            assert add_out.status_code == 400
            print("  ✓ Adding out-of-stock product blocked with HTTP 400.")
            passed_tests += 1
        finally:
            # Restore stock
            product.stock = original_stock
            db.session.commit()

        # Step 9: Move Product to Wishlist
        print("\n[TEST 9] Move Product from Cart to Wishlist")
        move_to_wish_res = client.post(f'/api/cart/{cart_item_id}/move-to-wishlist', headers=headers)
        assert move_to_wish_res.status_code == 200
        cart_data = move_to_wish_res.get_json()['cart']
        assert len(cart_data['items']) == 0
        print("  ✓ Item removed from cart.")

        wish_res = client.get('/api/wishlist', headers=headers)
        assert wish_res.status_code == 200
        wishlist = wish_res.get_json()['wishlist']
        assert any(w['product_id'] == product.id for w in wishlist)
        print(f"  ✓ '{product.name}' now present in wishlist.")
        passed_tests += 1

        # Step 10: Move Wishlist Product Back to Cart
        print("\n[TEST 10] Move Wishlist Product back to Cart")
        move_to_cart_res = client.post('/api/wishlist/move-to-cart', headers=headers, json={
            'product_id': product.id
        })
        assert move_to_cart_res.status_code == 200
        print(f"  ✓ Moved '{product.name}' from wishlist to cart.")

        wish_after = client.get('/api/wishlist', headers=headers).get_json()['wishlist']
        assert not any(w['product_id'] == product.id for w in wish_after)
        print("  ✓ Removed from wishlist after move.")

        cart_after = client.get('/api/cart', headers=headers).get_json()['cart']
        assert len(cart_after['items']) == 1
        print("  ✓ Product restored in shopping cart.")
        passed_tests += 1

        # Step 11: Cart Persistence in PostgreSQL Across Login Sessions
        print("\n[TEST 11] Cart Persistence in PostgreSQL Across Sessions")
        # Simulate logout / new login
        new_login = client.post('/api/auth/login', json={
            'email': test_email,
            'password': test_password
        })
        new_token = new_login.get_json()['token']
        new_headers = {'Authorization': f'Bearer {new_token}'}

        persisted_cart = client.get('/api/cart', headers=new_headers).get_json()['cart']
        assert len(persisted_cart['items']) == 1
        assert persisted_cart['items'][0]['product_id'] == product.id
        print("  ✓ Cart data verified intact in PostgreSQL across new authentication session.")
        passed_tests += 1

        # Step 12: Remove Product and Clear Cart
        print("\n[TEST 12] Remove Product and Clear Cart")
        remaining_item_id = persisted_cart['items'][0]['id']
        remove_res = client.delete(f'/api/cart/{remaining_item_id}', headers=new_headers)
        assert remove_res.status_code == 200
        empty_check = remove_res.get_json()['cart']
        assert len(empty_check['items']) == 0
        assert empty_check['items_count'] == 0
        assert empty_check['final_total'] == 0.0
        print("  ✓ Product successfully removed from cart.")

        # Test clear cart endpoint as well
        client.post('/api/cart', headers=new_headers, json={'product_id': product.id, 'quantity': 1})
        clear_res = client.post('/api/cart/clear', headers=new_headers)
        assert clear_res.status_code == 200
        assert len(clear_res.get_json()['cart']['items']) == 0
        print("  ✓ Cart cleared successfully via /api/cart/clear.")
        passed_tests += 1

    print("\n======================================================================")
    print(f"🎉 ALL {passed_tests}/{total_tests} PHASE 6 CART & WISHLIST TESTS PASSED!")
    print("======================================================================")
    return True

if __name__ == '__main__':
    success = run_tests()
    if not success:
        sys.exit(1)
