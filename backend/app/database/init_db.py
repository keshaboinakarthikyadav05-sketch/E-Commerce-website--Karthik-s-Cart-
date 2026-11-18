import re

import click
from flask import Flask
from sqlalchemy.engine import make_url

from app.models import Category, Product, ProductImage, ProductVariant, db
from seed.sample_products import CATEGORIES_DATA, PRODUCTS_DATA


def _slugify(value):
    return re.sub(r'[\s\W-]+', '-', value.lower().strip()).strip('-')


def seed_catalog():
    categories = {}
    for data in CATEGORIES_DATA:
        category = Category.query.filter_by(slug=data['slug']).first()
        if category is None:
            category = Category(
                name=data['name'],
                slug=data['slug'],
                description=data['description'],
                image_url=data['image_url'],
            )
            db.session.add(category)
            db.session.flush()
        categories[data['slug']] = category

    inserted_count = 0
    for data in PRODUCTS_DATA:
        slug = _slugify(data['name'])
        if Product.query.filter_by(slug=slug).first() is not None:
            continue

        category = categories.get(data['category_slug'])
        if category is None:
            raise RuntimeError(f"Missing sample category: {data['category_slug']}")

        original_price = float(data['original_price'])
        discounted_price = float(data['discounted_price'])
        discount_percent = (
            int(round((original_price - discounted_price) / original_price * 100))
            if original_price > 0 else 0
        )
        product = Product(
            name=data['name'],
            slug=slug,
            category_id=category.id,
            brand=data['brand'],
            original_price=original_price,
            discounted_price=discounted_price,
            discount_percent=discount_percent,
            stock=data['stock'],
            rating=data['rating'],
            num_reviews=data['num_reviews'],
            description=data['description'],
            specifications=data.get('specifications', {}),
            is_featured=data.get('is_featured', False),
            is_trending=data.get('is_trending', False),
            is_bestseller=data.get('is_bestseller', False),
        )
        db.session.add(product)
        db.session.flush()

        for order, image_url in enumerate(data.get('images', [])):
            db.session.add(ProductImage(
                product_id=product.id,
                image_url=image_url,
                is_primary=(order == 0),
                display_order=order,
            ))

        sizes = data.get('sizes', [])
        colors = data.get('colors', [])
        if sizes and colors:
            variants = ((size, color) for size in sizes[:3] for color in colors[:2])
        elif sizes:
            variants = ((size, None) for size in sizes)
        else:
            variants = ((None, color) for color in colors)

        for size, color in variants:
            color_code = re.sub(r'[^A-Z0-9]', '', (color or '').upper())
            variant_code = f"-{size}" if size else ''
            variant_code += f"-{color_code[:4]}" if color else ''
            db.session.add(ProductVariant(
                product_id=product.id,
                size=size,
                color=color,
                sku=f"{slug[:12].upper()}{variant_code}-{product.id}",
                additional_price=0,
                stock=15,
            ))
        inserted_count += 1

    return inserted_count


def initialize_database(app: Flask):
    if not app.config.get('AUTO_INITIALIZE_DATABASE', True):
        return

    with app.app_context():
        try:
            db.create_all()
            inserted_count = seed_catalog()
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        app.logger.info(
            'Database initialized; inserted %s missing sample products.',
            inserted_count,
        )


def register_database_commands(app: Flask):
    @app.cli.command('init-db')
    def init_db_command():
        """Create missing tables and insert missing sample catalog records."""
        initialize_database(app)
        click.echo('Database initialized without deleting existing data.')

    @app.cli.command('reset-db')
    def reset_db_command():
        """Reset a development SQLite database and reload the sample catalog."""
        database_url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
        if app.config.get('IS_PRODUCTION') or database_url.get_backend_name() != 'sqlite':
            raise click.ClickException('reset-db is allowed only for development SQLite databases.')

        with app.app_context():
            try:
                db.drop_all()
                db.create_all()
                inserted_count = seed_catalog()
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        click.echo(f'Development database reset; inserted {inserted_count} sample products.')
