import re
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_, desc, asc
from app.models import db, Product, Category, ProductImage, ProductVariant, Review, Order, OrderItem
from app.utils.auth_decorators import admin_required, customer_required
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

products_bp = Blueprint('products', __name__)

def slugify(text):
    text = text.lower().strip()
    return re.sub(r'[\s\W-]+', '-', text).strip('-')

def _search_pattern(value):
    escaped = value.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
    return f"%{escaped}%"

def _product_search_filter(value):
    pattern = _search_pattern(value)
    return or_(
        Product.name.ilike(pattern, escape='\\'),
        Product.brand.ilike(pattern, escape='\\'),
        Product.description.ilike(pattern, escape='\\'),
        Product.category.has(or_(
            Category.name.ilike(pattern, escape='\\'),
            Category.slug.ilike(pattern, escape='\\'),
        )),
    )

@products_bp.route('', methods=['GET'])
def get_products():
    try:
        page = int(request.args.get('page', '1'))
        limit = int(request.args.get('limit', '12'))
    except ValueError:
        return jsonify({'success': False, 'message': 'Page and limit must be integers'}), 400
    if page < 1 or limit < 1 or limit > 100:
        return jsonify({'success': False, 'message': 'Page must be positive and limit must be between 1 and 100'}), 400

    search = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    brand = request.args.get('brand', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    rating = request.args.get('rating', type=float)
    sort = request.args.get('sort', 'newest').strip()
    featured = request.args.get('featured', type=str)
    trending = request.args.get('trending', type=str)
    bestseller = request.args.get('bestseller', type=str)

    query = Product.query

    # Search filter
    if search:
        query = query.filter(_product_search_filter(search))

    # Category filter (by slug or id)
    if category:
        if category.isdigit():
            query = query.filter(Product.category_id == int(category))
        else:
            cat = Category.query.filter(
                or_(
                    Category.slug.ilike(category),
                    Category.name.ilike(_search_pattern(category), escape='\\'),
                )
            ).first()
            if cat:
                query = query.filter(Product.category_id == cat.id)
            else:
                # Filter by name ilike
                query = query.join(Category).filter(Category.name.ilike(category))

    # Brand filter (supports comma-separated brands)
    if brand:
        brands = [b.strip() for b in brand.split(',') if b.strip()]
        if len(brands) == 1:
            query = query.filter(Product.brand.ilike(brands[0]))
        elif len(brands) > 1:
            query = query.filter(Product.brand.in_(brands))

    # Price range filter
    if min_price is not None:
        query = query.filter(Product.discounted_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.discounted_price <= max_price)

    # Rating filter
    if rating is not None:
        query = query.filter(Product.rating >= rating)

    # Flags
    if featured and featured.lower() in ('true', '1'):
        query = query.filter(Product.is_featured == True)
    if trending and trending.lower() in ('true', '1'):
        query = query.filter(Product.is_trending == True)
    if bestseller and bestseller.lower() in ('true', '1'):
        query = query.filter(Product.is_bestseller == True)

    # Sorting
    if sort == 'price_asc':
        query = query.order_by(Product.discounted_price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.discounted_price.desc())
    elif sort == 'popularity':
        query = query.order_by(Product.rating.desc(), Product.num_reviews.desc())
    elif sort == 'discount':
        query = query.order_by(Product.discount_percent.desc())
    else: # newest
        query = query.order_by(Product.created_at.desc())

    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        'success': True,
        'products': [p.to_dict(include_details=False) for p in paginated.items],
        'pagination': {
            'total': paginated.total,
            'page': paginated.page,
            'pages': paginated.pages,
            'limit': paginated.per_page,
            'has_prev': paginated.has_prev,
            'has_next': paginated.has_next
        }
    }), 200

@products_bp.route('/search', methods=['GET'])
def search_products():
    return get_products()

@products_bp.route('/search/suggestions', methods=['GET'])
def search_suggestions():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify({'success': True, 'suggestions': []}), 200

    matches = Product.query.filter(_product_search_filter(q)).order_by(
        Product.is_featured.desc(),
        Product.rating.desc(),
    ).limit(6).all()

    results = []
    for p in matches:
        results.append({
            'id': p.id,
            'name': p.name,
            'brand': p.brand,
            'category': p.category.name if p.category else '',
            'price': float(p.discounted_price),
            'image': p.images[0].image_url if p.images else None
        })

    return jsonify({'success': True, 'suggestions': results}), 200

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    # Fetch related products from same category
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(6).all()

    # Fetch reviews
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()

    product_data = product.to_dict(include_details=True)
    product_data['related_products'] = [r.to_dict(include_details=False) for r in related]
    product_data['reviews'] = [rev.to_dict() for rev in reviews]

    return jsonify({'success': True, 'product': product_data}), 200

@products_bp.route('', methods=['POST'])
@admin_required()
def create_product():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    category_id = data.get('category_id')
    brand = data.get('brand', '').strip()
    original_price = data.get('original_price')
    discounted_price = data.get('discounted_price')
    description = data.get('description', '').strip()
    stock = data.get('stock', 10)
    specifications = data.get('specifications', {})
    images = data.get('images', [])
    variants = data.get('variants', [])
    is_featured = bool(data.get('is_featured', False))
    is_trending = bool(data.get('is_trending', False))
    is_bestseller = bool(data.get('is_bestseller', False))

    if not all([name, category_id, brand, original_price, discounted_price, description]):
        return jsonify({'success': False, 'message': 'Missing required product fields'}), 400

    orig_p = float(original_price)
    disc_p = float(discounted_price)
    discount_pct = int(round(((orig_p - disc_p) / orig_p) * 100)) if orig_p > 0 else 0

    slug_base = slugify(name)
    slug = slug_base
    counter = 1
    while Product.query.filter_by(slug=slug).first():
        slug = f"{slug_base}-{counter}"
        counter += 1

    try:
        product = Product(
            name=name,
            slug=slug,
            category_id=int(category_id),
            brand=brand,
            original_price=orig_p,
            discounted_price=disc_p,
            discount_percent=max(0, discount_pct),
            description=description,
            stock=int(stock),
            specifications=specifications,
            is_featured=is_featured,
            is_trending=is_trending,
            is_bestseller=is_bestseller
        )
        db.session.add(product)
        db.session.flush()

        # Add images
        if isinstance(images, list):
            for idx, img in enumerate(images):
                img_url = img if isinstance(img, str) else img.get('image_url')
                is_pri = (idx == 0) if isinstance(img, str) else img.get('is_primary', idx == 0)
                if img_url:
                    p_img = ProductImage(
                        product_id=product.id,
                        image_url=img_url,
                        is_primary=is_pri,
                        display_order=idx
                    )
                    db.session.add(p_img)

        # Add variants
        if isinstance(variants, list):
            for v in variants:
                p_var = ProductVariant(
                    product_id=product.id,
                    size=v.get('size'),
                    color=v.get('color'),
                    sku=v.get('sku', f"{slug}-{v.get('size', '')}-{v.get('color', '')}"),
                    additional_price=float(v.get('additional_price', 0.0)),
                    stock=int(v.get('stock', 10))
                )
                db.session.add(p_var)

        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'product': product.to_dict(include_details=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to create product', 'error': str(e)}), 500

@products_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    data = request.get_json() or {}
    if 'name' in data:
        product.name = data['name']
    if 'brand' in data:
        product.brand = data['brand']
    if 'category_id' in data:
        product.category_id = int(data['category_id'])
    if 'description' in data:
        product.description = data['description']
    if 'stock' in data:
        product.stock = int(data['stock'])
    if 'original_price' in data:
        product.original_price = float(data['original_price'])
    if 'discounted_price' in data:
        product.discounted_price = float(data['discounted_price'])
        if product.original_price > 0:
            product.discount_percent = int(round(((float(product.original_price) - float(product.discounted_price)) / float(product.original_price)) * 100))
    if 'specifications' in data:
        product.specifications = data['specifications']
    if 'is_featured' in data:
        product.is_featured = bool(data['is_featured'])
    if 'is_trending' in data:
        product.is_trending = bool(data['is_trending'])
    if 'is_bestseller' in data:
        product.is_bestseller = bool(data['is_bestseller'])

    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Product updated successfully',
        'product': product.to_dict(include_details=True)
    }), 200

@products_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Product deleted successfully'}), 200

@products_bp.route('/<int:id>/reviews', methods=['POST'])
@customer_required()
def add_review(id):
    user_id = int(get_jwt_identity())
    product = Product.query.get(id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    data = request.get_json() or {}
    rating = data.get('rating')
    comment = data.get('comment', '').strip()
    title = data.get('title', '').strip()

    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({'success': False, 'message': 'Rating must be an integer between 1 and 5'}), 400
    if not comment:
        return jsonify({'success': False, 'message': 'Review comment is required'}), 400

    from app.models.user import User
    user = User.query.get(user_id)

    review = Review(
        product_id=product.id,
        user_id=user_id,
        rating=int(rating),
        title=title,
        comment=comment,
        user_name=user.full_name if user else 'Verified Shopper',
        is_verified_purchase=True
    )
    db.session.add(review)

    # Recalculate average rating
    all_reviews = Review.query.filter_by(product_id=product.id).all()
    total_ratings = sum(r.rating for r in all_reviews) + int(rating)
    count = len(all_reviews) + 1
    product.rating = round(total_ratings / count, 2)
    product.num_reviews = count

    db.session.commit()
    return jsonify({'success': True, 'message': 'Review submitted', 'review': review.to_dict()}), 201
