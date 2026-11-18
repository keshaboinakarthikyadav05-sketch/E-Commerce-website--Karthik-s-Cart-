from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import db, Wishlist, Product, CartItem, ProductVariant
from app.utils.auth_decorators import customer_required

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('', methods=['GET'])
@customer_required()
def get_wishlist():
    user_id = int(get_jwt_identity())
    items = Wishlist.query.filter_by(user_id=user_id).order_by(Wishlist.created_at.desc()).all()
    
    serialized = []
    for item in items:
        data = item.to_dict()
        if item.product:
            data['is_out_of_stock'] = (item.product.stock <= 0)
            data['stock'] = item.product.stock
        serialized.append(data)

    return jsonify({
        'success': True,
        'wishlist': serialized,
        'count': len(items)
    }), 200

@wishlist_bp.route('', methods=['POST'])
@customer_required()
def add_to_wishlist():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    existing = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify({
            'success': True,
            'message': f"'{product.name}' is already in your wishlist",
            'item': existing.to_dict()
        }), 200

    item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(item)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"Added '{product.name}' to your wishlist",
        'item': item.to_dict(),
        'count': Wishlist.query.filter_by(user_id=user_id).count()
    }), 201

@wishlist_bp.route('/<int:product_id>', methods=['DELETE'])
@customer_required()
def remove_from_wishlist(product_id):
    user_id = int(get_jwt_identity())
    item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        return jsonify({'success': False, 'message': 'Item not found in wishlist'}), 404

    prod_name = item.product.name if item.product else 'Product'
    db.session.delete(item)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"Removed '{prod_name}' from wishlist",
        'count': Wishlist.query.filter_by(user_id=user_id).count()
    }), 200

@wishlist_bp.route('/move-to-cart', methods=['POST'])
@customer_required()
def move_to_cart():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    product_id = data.get('product_id')
    size = data.get('size')
    color = data.get('color')

    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    # Stock validation
    if product.stock <= 0:
        return jsonify({
            'success': False,
            'message': f"Cannot move '{product.name}' to cart because it is currently out of stock."
        }), 400

    # Auto-pick first available size/color from variants if not specified
    if not size and product.variants:
        available_sizes = [v.size for v in product.variants if v.size]
        if available_sizes:
            size = available_sizes[0]
    if not color and product.variants:
        available_colors = [v.color for v in product.variants if v.color]
        if available_colors:
            color = available_colors[0]

    # Find matching variant
    variant = None
    if size or color:
        query = ProductVariant.query.filter_by(product_id=product_id)
        if size:
            query = query.filter_by(size=size)
        if color:
            query = query.filter_by(color=color)
        variant = query.first()

    # Check if existing cart item matches
    existing_cart = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product_id,
        size=size,
        color=color
    ).first()

    if existing_cart:
        if existing_cart.quantity + 1 > product.stock:
            return jsonify({
                'success': False,
                'message': f"You already have {existing_cart.quantity} of '{product.name}' in cart, reaching the stock limit."
            }), 400
        existing_cart.quantity += 1
    else:
        new_cart = CartItem(
            user_id=user_id,
            product_id=product_id,
            variant_id=variant.id if variant else None,
            size=size,
            color=color,
            quantity=1
        )
        db.session.add(new_cart)

    # Remove from wishlist
    Wishlist.query.filter_by(user_id=user_id, product_id=product_id).delete()

    db.session.commit()
    return jsonify({
        'success': True,
        'message': f"Moved '{product.name}' to your cart",
        'wishlist_count': Wishlist.query.filter_by(user_id=user_id).count()
    }), 200
