import os
import sys
import re
from datetime import datetime, timedelta

# Add backend directory to sys.path so app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import (
    db, User, Address, Category, Product, ProductImage, ProductVariant,
    CartItem, Wishlist, Order, OrderItem, Payment, Review, Coupon
)
from seed.sample_products import CATEGORIES_DATA, PRODUCTS_DATA

def slugify(text):
    text = text.lower().strip()
    return re.sub(r'[\s\W-]+', '-', text).strip('-')

def seed_database():
    app = create_app()

    with app.app_context():
        print("🔧 Creating all PostgreSQL database tables...")
        db.create_all()
        print("✅ Database tables created successfully.")

        # 1. Seed Admin User
        admin = User.query.filter_by(email='admin@shopora.com').first()
        if not admin:
            admin = User(
                full_name='SHOPORA Administrator',
                email='admin@shopora.com',
                mobile_number='+91 9876543210',
                role='admin',
                is_active=True
            )
            admin.set_password('Admin@123')
            db.session.add(admin)
            print("👤 Admin user seeded: admin@shopora.com / Admin@123")

        # 2. Seed Customer User
        customer = User.query.filter_by(email='customer@shopora.com').first()
        if not customer:
            customer = User(
                full_name='Aarav Sharma',
                email='customer@shopora.com',
                mobile_number='+91 9811223344',
                role='customer',
                is_active=True
            )
            customer.set_password('Customer@123')
            db.session.add(customer)
            db.session.flush()

            # Add default address
            address = Address(
                user_id=customer.id,
                full_name='Aarav Sharma',
                mobile_number='+91 9811223344',
                address_line1='Flat 402, Skyline Residency, Indiranagar',
                address_line2='100 Feet Road, Near Metro Station',
                city='Bengaluru',
                state='Karnataka',
                postal_code='560038',
                country='India',
                is_default=True
            )
            db.session.add(address)
            print("👤 Demo customer seeded: customer@shopora.com / Customer@123")

        # 3. Seed Coupons
        coupons = [
            {
                'code': 'Karthik10',
                'description': 'Flat 10% instant discount on all orders',
                'discount_type': 'percentage',
                'discount_value': 10.0,
                'min_order_amount': 500.0,
                'max_discount': 1500.0,
                'valid_until': datetime.utcnow() + timedelta(days=365)
            },
            {
                'code': 'WELCOME200',
                'description': 'Flat ₹200 off on your first order above ₹1,000',
                'discount_type': 'fixed',
                'discount_value': 200.0,
                'min_order_amount': 1000.0,
                'max_discount': 200.0,
                'valid_until': datetime.utcnow() + timedelta(days=180)
            },
            {
                'code': 'FESTIVE500',
                'description': 'Special festive ₹500 off on orders above ₹2,500',
                'discount_type': 'fixed',
                'discount_value': 500.0,
                'min_order_amount': 2500.0,
                'max_discount': 500.0,
                'valid_until': datetime.utcnow() + timedelta(days=90)
            }
        ]

        for c_data in coupons:
            if not Coupon.query.filter_by(code=c_data['code']).first():
                coupon = Coupon(**c_data)
                db.session.add(coupon)
        print(f"🎟️ Seeded {len(coupons)} discount coupons.")

        # 4. Seed Categories
        category_map = {}
        for cat_info in CATEGORIES_DATA:
            category = Category.query.filter_by(slug=cat_info['slug']).first()
            if not category:
                category = Category(
                    name=cat_info['name'],
                    slug=cat_info['slug'],
                    description=cat_info['description'],
                    image_url=cat_info['image_url']
                )
                db.session.add(category)
                db.session.flush()
            category_map[cat_info['slug']] = category
        print(f"📁 Seeded {len(CATEGORIES_DATA)} product categories.")

        # 5. Clean up any renamed or deleted products
        valid_slugs = {slugify(p['name']) for p in PRODUCTS_DATA}
        obsolete_prods = Product.query.filter(~Product.slug.in_(valid_slugs)).all()
        for op in obsolete_prods:
            ProductImage.query.filter_by(product_id=op.id).delete()
            ProductVariant.query.filter_by(product_id=op.id).delete()
            CartItem.query.filter_by(product_id=op.id).delete()
            Wishlist.query.filter_by(product_id=op.id).delete()
            db.session.delete(op)
        if obsolete_prods:
            db.session.commit()
            print(f"🧹 Cleaned up {len(obsolete_prods)} renamed/obsolete products.")

        # 6. Seed / Update Products
        products_seeded_count = 0
        for p_data in PRODUCTS_DATA:
            cat_slug = p_data['category_slug']
            category = category_map.get(cat_slug)
            if not category:
                continue

            orig_price = float(p_data['original_price'])
            disc_price = float(p_data['discounted_price'])
            disc_pct = int(round(((orig_price - disc_price) / orig_price) * 100)) if orig_price > 0 else 0

            base_slug = slugify(p_data['name'])
            existing_prod = Product.query.filter_by(slug=base_slug).first()
            if existing_prod:
                existing_prod.brand = p_data['brand']
                existing_prod.original_price = orig_price
                existing_prod.discounted_price = disc_price
                existing_prod.discount_percent = disc_pct
                existing_prod.stock = p_data['stock']
                existing_prod.rating = p_data['rating']
                existing_prod.num_reviews = p_data['num_reviews']
                existing_prod.description = p_data['description']
                existing_prod.specifications = p_data.get('specifications', {})
                existing_prod.is_featured = p_data.get('is_featured', False)
                existing_prod.is_trending = p_data.get('is_trending', False)
                existing_prod.is_bestseller = p_data.get('is_bestseller', False)

                # Update images
                new_images = p_data.get('images', [])
                if new_images:
                    ProductImage.query.filter_by(product_id=existing_prod.id).delete()
                    for idx, img_url in enumerate(new_images):
                        p_img = ProductImage(
                            product_id=existing_prod.id,
                            image_url=img_url,
                            is_primary=(idx == 0),
                            display_order=idx
                        )
                        db.session.add(p_img)
                products_seeded_count += 1
                continue

            product = Product(
                name=p_data['name'],
                slug=base_slug,
                category_id=category.id,
                brand=p_data['brand'],
                original_price=orig_price,
                discounted_price=disc_price,
                discount_percent=disc_pct,
                stock=p_data['stock'],
                rating=p_data['rating'],
                num_reviews=p_data['num_reviews'],
                description=p_data['description'],
                specifications=p_data.get('specifications', {}),
                is_featured=p_data.get('is_featured', False),
                is_trending=p_data.get('is_trending', False),
                is_bestseller=p_data.get('is_bestseller', False)
            )
            db.session.add(product)
            db.session.flush()

            # Seed Images
            for idx, img_url in enumerate(p_data.get('images', [])):
                p_img = ProductImage(
                    product_id=product.id,
                    image_url=img_url,
                    is_primary=(idx == 0),
                    display_order=idx
                )
                db.session.add(p_img)

            # Seed Variants
            sizes = p_data.get('sizes', [])
            colors = p_data.get('colors', [])
            
            if sizes and colors:
                for s in sizes[:3]: # top 3 sizes
                    for c in colors[:2]: # top 2 colors
                        clean_c = re.sub(r'[^A-Z0-9]', '', c.upper())
                        v = ProductVariant(
                            product_id=product.id,
                            size=s,
                            color=c,
                            sku=f"{base_slug[:10].upper()}-{s}-{clean_c[:4]}-{product.id}",
                            additional_price=0.00,
                            stock=15
                        )
                        db.session.add(v)
            elif sizes:
                for s in sizes:
                    v = ProductVariant(
                        product_id=product.id,
                        size=s,
                        color=None,
                        sku=f"{base_slug[:12].upper()}-{s}-{product.id}",
                        additional_price=0.00,
                        stock=15
                    )
                    db.session.add(v)
            elif colors:
                for c in colors:
                    clean_c = re.sub(r'[^A-Z0-9]', '', c.upper())
                    v = ProductVariant(
                        product_id=product.id,
                        size=None,
                        color=c,
                        sku=f"{base_slug[:12].upper()}-{clean_c[:4]}-{product.id}",
                        additional_price=0.00,
                        stock=15
                    )
                    db.session.add(v)

            # Add sample reviews for top products
            sample_review = Review(
                product_id=product.id,
                user_id=customer.id if customer else 1,
                rating=5 if product.rating >= 4.7 else 4,
                title="Superb quality! Exceeded expectations",
                comment=f"I purchased this {product.name} recently and the build quality, materials, and finish are top notch. Delivery by Shopora was remarkably quick!",
                user_name="Aarav Sharma",
                is_verified_purchase=True
            )
            db.session.add(sample_review)

            products_seeded_count += 1

        db.session.commit()
        print(f"🛍️ Seeded {products_seeded_count} products with images and variants (Total in DB: {Product.query.count()}).")

        # 6. Seed Sample Initial Orders for Admin Dashboard Analytics
        if Order.query.count() == 0 and customer:
            sample_products = Product.query.limit(3).all()
            if sample_products:
                order1 = Order(
                    order_number="SHOP-20261115-DEMO01",
                    user_id=customer.id,
                    shipping_name="Aarav Sharma",
                    shipping_mobile="+91 9811223344",
                    shipping_address_text="Flat 402, Skyline Residency, Indiranagar",
                    shipping_city="Bengaluru",
                    shipping_state="Karnataka",
                    shipping_postal_code="560038",
                    subtotal=float(sample_products[0].discounted_price),
                    discount=0.0,
                    delivery_charge=0.0,
                    total_amount=float(sample_products[0].discounted_price),
                    payment_method="razorpay",
                    payment_status="paid",
                    order_status="delivered",
                    razorpay_order_id="order_demo_12345",
                    razorpay_payment_id="pay_demo_98765",
                    created_at=datetime.utcnow() - timedelta(days=2)
                )
                db.session.add(order1)
                db.session.flush()

                oi1 = OrderItem(
                    order_id=order1.id,
                    product_id=sample_products[0].id,
                    product_name=sample_products[0].name,
                    product_image=sample_products[0].images[0].image_url if sample_products[0].images else None,
                    price=float(sample_products[0].discounted_price),
                    quantity=1,
                    size="32" if sample_products[0].variants else None,
                    color="Blue" if sample_products[0].variants else None,
                    total_price=float(sample_products[0].discounted_price)
                )
                db.session.add(oi1)

                pay1 = Payment(
                    order_id=order1.id,
                    razorpay_order_id="order_demo_12345",
                    razorpay_payment_id="pay_demo_98765",
                    amount=order1.total_amount,
                    currency="INR",
                    status="captured",
                    method="razorpay"
                )
                db.session.add(pay1)

                db.session.commit()
                print("📦 Seeded sample order for dashboard analytics.")

        print("🎉 Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
