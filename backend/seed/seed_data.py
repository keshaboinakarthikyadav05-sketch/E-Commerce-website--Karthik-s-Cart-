import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import Address, Coupon, Order, OrderItem, Payment, Product, User, db


def seed_database():
    app = create_app()

    with app.app_context():
        seed_demo_users = os.getenv('SEED_DEMO_USERS', 'false').lower() == 'true'
        customer = None

        if seed_demo_users:
            admin_email = os.getenv('SEED_ADMIN_EMAIL')
            admin_password = os.getenv('SEED_ADMIN_PASSWORD')
            customer_email = os.getenv('SEED_CUSTOMER_EMAIL')
            customer_password = os.getenv('SEED_CUSTOMER_PASSWORD')
            if not all([admin_email, admin_password, customer_email, customer_password]):
                raise RuntimeError(
                    'SEED_DEMO_USERS requires SEED_ADMIN_EMAIL, SEED_ADMIN_PASSWORD, '
                    'SEED_CUSTOMER_EMAIL, and SEED_CUSTOMER_PASSWORD.'
                )

            admin = User.query.filter_by(email=admin_email).first()
            if not admin:
                admin = User(
                    full_name='SHOPORA Administrator',
                    email=admin_email,
                    mobile_number='+91 9876543210',
                    role='admin',
                    is_active=True,
                )
                admin.set_password(admin_password)
                db.session.add(admin)

            customer = User.query.filter_by(email=customer_email).first()
            if not customer:
                customer = User(
                    full_name='Aarav Sharma',
                    email=customer_email,
                    mobile_number='+91 9811223344',
                    role='customer',
                    is_active=True,
                )
                customer.set_password(customer_password)
                db.session.add(customer)
                db.session.flush()
                db.session.add(Address(
                    user_id=customer.id,
                    full_name='Aarav Sharma',
                    mobile_number='+91 9811223344',
                    address_line1='Flat 402, Skyline Residency, Indiranagar',
                    address_line2='100 Feet Road, Near Metro Station',
                    city='Bengaluru',
                    state='Karnataka',
                    postal_code='560038',
                    country='India',
                    is_default=True,
                ))

        now = datetime.utcnow()
        coupons = [
            Coupon(
                code='SHOPORA10',
                description='Flat 10% instant discount on all orders',
                discount_type='percentage',
                discount_value=10.0,
                min_order_amount=500.0,
                max_discount=1500.0,
                valid_until=now + timedelta(days=365),
            ),
            Coupon(
                code='WELCOME200',
                description='Flat ₹200 off on your first order above ₹1,000',
                discount_type='fixed',
                discount_value=200.0,
                min_order_amount=1000.0,
                max_discount=200.0,
                valid_until=now + timedelta(days=180),
            ),
            Coupon(
                code='FESTIVE500',
                description='Special festive ₹500 off on orders above ₹2,500',
                discount_type='fixed',
                discount_value=500.0,
                min_order_amount=2500.0,
                max_discount=500.0,
                valid_until=now + timedelta(days=90),
            ),
        ]
        for coupon in coupons:
            if not Coupon.query.filter_by(code=coupon.code).first():
                db.session.add(coupon)
        db.session.commit()

        if seed_demo_users and customer and Order.query.count() == 0:
            product = Product.query.first()
            if product:
                order = Order(
                    order_number='SHOP-DEMO-INITIAL',
                    user_id=customer.id,
                    shipping_name='Aarav Sharma',
                    shipping_mobile='+91 9811223344',
                    shipping_address_text='Flat 402, Skyline Residency, Indiranagar',
                    shipping_city='Bengaluru',
                    shipping_state='Karnataka',
                    shipping_postal_code='560038',
                    subtotal=float(product.discounted_price),
                    discount=0.0,
                    delivery_charge=0.0,
                    total_amount=float(product.discounted_price),
                    payment_method='razorpay',
                    payment_status='paid',
                    order_status='delivered',
                    razorpay_order_id='order_demo_initial',
                    razorpay_payment_id='pay_demo_initial',
                    created_at=now - timedelta(days=2),
                )
                db.session.add(order)
                db.session.flush()
                db.session.add(OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    product_image=product.images[0].image_url if product.images else None,
                    price=float(product.discounted_price),
                    quantity=1,
                    total_price=float(product.discounted_price),
                ))
                db.session.add(Payment(
                    order_id=order.id,
                    razorpay_order_id=order.razorpay_order_id,
                    razorpay_payment_id=order.razorpay_payment_id,
                    amount=order.total_amount,
                    currency='INR',
                    status='captured',
                    method='razorpay',
                ))
                db.session.commit()

        print(f"Database ready: {Product.query.count()} products.")


if __name__ == '__main__':
    seed_database()
