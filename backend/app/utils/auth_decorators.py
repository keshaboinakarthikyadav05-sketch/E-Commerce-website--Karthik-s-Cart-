from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def customer_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(int(user_id))
                if not user or not user.is_active:
                    return jsonify({'success': False, 'message': 'User account is inactive or not found'}), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'success': False, 'message': 'Authentication required or token expired', 'error': str(e)}), 401
        return decorator
    return wrapper

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(int(user_id))
                if not user or user.role != 'admin':
                    return jsonify({'success': False, 'message': 'Administrator access required'}), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'success': False, 'message': 'Admin authentication required', 'error': str(e)}), 401
        return decorator
    return wrapper
