from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

from .user import User, Address
from .category import Category
from .product import Product, ProductImage, ProductVariant
from .cart import CartItem, Wishlist
from .order import Order, OrderItem
from .payment import Payment
from .review import Review
from .coupon import Coupon

__all__ = [
    'db',
    'bcrypt',
    'jwt',
    'User',
    'Address',
    'Category',
    'Product',
    'ProductImage',
    'ProductVariant',
    'CartItem',
    'Wishlist',
    'Order',
    'OrderItem',
    'Payment',
    'Review',
    'Coupon'
]
