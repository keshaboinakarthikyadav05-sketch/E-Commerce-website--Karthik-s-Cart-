import re
from flask import Blueprint, request, jsonify
from app.models import db, Category, Product
from app.utils.auth_decorators import admin_required

categories_bp = Blueprint('categories', __name__)

def slugify(text):
    text = text.lower().strip()
    return re.sub(r'[\s\W-]+', '-', text).strip('-')

@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({
        'success': True,
        'categories': [c.to_dict() for c in categories]
    }), 200

@categories_bp.route('/<string:slug>', methods=['GET'])
def get_category_by_slug(slug):
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        return jsonify({'success': False, 'message': 'Category not found'}), 404
    return jsonify({
        'success': True,
        'category': category.to_dict()
    }), 200

@categories_bp.route('', methods=['POST'])
@admin_required()
def create_category():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    image_url = data.get('image_url', '').strip()

    if not name:
        return jsonify({'success': False, 'message': 'Category name is required'}), 400

    slug = slugify(name)
    existing = Category.query.filter((Category.name == name) | (Category.slug == slug)).first()
    if existing:
        return jsonify({'success': False, 'message': 'Category with this name or slug already exists'}), 409

    category = Category(name=name, slug=slug, description=description, image_url=image_url)
    db.session.add(category)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Category created successfully',
        'category': category.to_dict()
    }), 201

@categories_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'success': False, 'message': 'Category not found'}), 404

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if name and name != category.name:
        category.name = name
        category.slug = slugify(name)
    if 'description' in data:
        category.description = data.get('description')
    if 'image_url' in data:
        category.image_url = data.get('image_url')

    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Category updated successfully',
        'category': category.to_dict()
    }), 200

@categories_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'success': False, 'message': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Category deleted successfully'}), 200
