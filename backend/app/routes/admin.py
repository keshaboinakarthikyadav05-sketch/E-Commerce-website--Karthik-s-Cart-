from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.models import db, User, Product, Order, OrderItem, Category
from app.utils.auth_decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required()
def get_dashboard_stats():
    # Overall summary stats
    total_users = User.query.filter_by(role='customer').count()
    total_products = Product.query.count()
    total_orders = Order.query.count()

    total_sales_result = db.session.query(func.sum(Order.total_amount))\
        .filter(Order.payment_status == 'paid').scalar()
    total_sales = float(total_sales_result or 0.0)

    # Count out of stock products
    low_stock_count = Product.query.filter(Product.stock <= 5).count()

    # Recent orders (latest 8)
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()

    # Sales trends over the past 7 days for charts
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_sales = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('total'),
        func.count(Order.id).label('orders_count')
    ).filter(
        Order.created_at >= seven_days_ago,
        Order.payment_status.in_(['paid', 'pending'])
    ).group_by(func.date(Order.created_at)).order_by('date').all()

    sales_chart = []
    for s in daily_sales:
        sales_chart.append({
            'date': str(s.date),
            'sales': float(s.total or 0.0),
            'orders': int(s.orders_count or 0)
        })

    # Orders distribution by status
    status_counts = db.session.query(
        Order.order_status,
        func.count(Order.id)
    ).group_by(Order.order_status).all()

    status_dist = {status: count for status, count in status_counts}

    # Category distribution
    cat_counts = db.session.query(
        Category.name,
        func.count(Product.id)
    ).join(Product, Product.category_id == Category.id)\
     .group_by(Category.name).all()

    category_dist = [{'category': name, 'count': count} for name, count in cat_counts]

    return jsonify({
        'success': True,
        'stats': {
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_sales': round(total_sales, 2),
            'low_stock_count': low_stock_count,
            'status_distribution': status_dist,
            'category_distribution': category_dist,
            'sales_chart': sales_chart,
            'recent_orders': [o.to_dict() for o in recent_orders]
        }
    }), 200

@admin_bp.route('/orders', methods=['GET'])
@admin_required()
def get_admin_orders():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 15, type=int)
    status = request.args.get('status', '').strip()

    query = Order.query
    if status:
        query = query.filter_by(order_status=status)

    paginated = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        'success': True,
        'orders': [o.to_dict() for o in paginated.items],
        'pagination': {
            'total': paginated.total,
            'page': paginated.page,
            'pages': paginated.pages,
            'limit': paginated.per_page
        }
    }), 200

@admin_bp.route('/orders/<int:id>/status', methods=['PUT'])
@admin_required()
def update_order_status(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'success': False, 'message': 'Order not found'}), 404

    data = request.get_json() or {}
    new_status = data.get('status', '').strip().lower()
    allowed_statuses = ['placed', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']

    if new_status not in allowed_statuses:
        return jsonify({'success': False, 'message': f'Invalid status. Allowed: {", ".join(allowed_statuses)}'}), 400

    order.order_status = new_status
    if 'payment_status' in data:
        order.payment_status = data['payment_status']

    db.session.commit()
    return jsonify({
        'success': True,
        'message': f'Order status updated to {new_status}',
        'order': order.to_dict()
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required()
def get_users():
    users = User.query.order_by(User.created_at.desc()).all()
    result = []
    for u in users:
        u_dict = u.to_dict()
        u_dict['orders_count'] = Order.query.filter_by(user_id=u.id).count()
        result.append(u_dict)

    return jsonify({
        'success': True,
        'users': result
    }), 200

@admin_bp.route('/users/<int:id>/toggle-status', methods=['PUT'])
@admin_required()
def toggle_user_status(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    if user.role == 'admin':
        return jsonify({'success': False, 'message': 'Cannot deactivate admin accounts'}), 400

    user.is_active = not user.is_active
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"User account {'activated' if user.is_active else 'deactivated'}",
        'user': user.to_dict()
    }), 200
