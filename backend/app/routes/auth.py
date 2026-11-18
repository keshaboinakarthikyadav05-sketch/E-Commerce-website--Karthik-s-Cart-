import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import db, User, Address
from app.utils.auth_decorators import customer_required

auth_bp = Blueprint('auth', __name__)

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    full_name = (data.get('full_name') or data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    mobile_number = (data.get('mobile_number') or data.get('phone') or '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not full_name:
        return jsonify({'success': False, 'message': 'Full name is required'}), 400
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'success': False, 'message': 'Valid email address is required'}), 400
    
    # If mobile is omitted, use a default fallback to prevent registration blockage
    if not mobile_number:
        mobile_number = '+91 9876543210'

    if not password or len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
    if confirm_password and password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'An account with this email already exists'}), 409

    try:
        user = User(
            full_name=full_name,
            email=email,
            mobile_number=mobile_number,
            role='customer'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'success': True,
            'message': 'Account registered successfully',
            'token': access_token,
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = (data.get('email') or data.get('username') or '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'success': False, 'message': 'Your account has been deactivated. Please contact support.'}), 403

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'success': True,
        'message': 'Logged in successfully',
        'token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
@customer_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    addresses = [a.to_dict() for a in user.addresses]
    user_data = user.to_dict()
    user_data['addresses'] = addresses
    return jsonify({'success': True, 'user': user_data}), 200

@auth_bp.route('/addresses', methods=['GET'])
@customer_required()
def get_addresses():
    user_id = get_jwt_identity()
    addresses = Address.query.filter_by(user_id=int(user_id)).all()
    return jsonify({'success': True, 'addresses': [a.to_dict() for a in addresses]}), 200

@auth_bp.route('/addresses', methods=['POST'])
@customer_required()
def add_address():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    full_name = data.get('full_name', '').strip()
    mobile_number = data.get('mobile_number', '').strip()
    address_line1 = data.get('address_line1', '').strip()
    address_line2 = data.get('address_line2', '').strip()
    city = data.get('city', '').strip()
    state = data.get('state', '').strip()
    postal_code = data.get('postal_code', '').strip()
    is_default = bool(data.get('is_default', False))

    if not all([full_name, mobile_number, address_line1, city, state, postal_code]):
        return jsonify({'success': False, 'message': 'Missing required address fields'}), 400

    if is_default:
        Address.query.filter_by(user_id=user_id).update({'is_default': False})

    new_address = Address(
        user_id=user_id,
        full_name=full_name,
        mobile_number=mobile_number,
        address_line1=address_line1,
        address_line2=address_line2,
        city=city,
        state=state,
        postal_code=postal_code,
        country='India',
        is_default=is_default
    )
    db.session.add(new_address)
    db.session.commit()

    return jsonify({'success': True, 'address': new_address.to_dict(), 'message': 'Address saved'}), 201
