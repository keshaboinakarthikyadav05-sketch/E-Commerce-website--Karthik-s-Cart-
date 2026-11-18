from datetime import datetime
from . import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id', ondelete='SET NULL'), nullable=True)
    size = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    product = db.relationship('Product', lazy='joined')
    variant = db.relationship('ProductVariant', lazy='joined')

    def to_dict(self):
        unit_price = float(self.product.discounted_price) if self.product else 0.0
        if self.variant and self.variant.additional_price:
            unit_price += float(self.variant.additional_price)

        stock = self.product.stock if self.product else 0
        is_out_of_stock = (stock <= 0)
        exceeds_stock = (self.quantity > stock) if stock > 0 else True
        is_low_stock = (0 < stock <= 5)

        sizes = []
        colors = []
        if self.product and self.product.variants:
            sizes = sorted(list({v.size for v in self.product.variants if v.size}))
            colors = sorted(list({v.color for v in self.product.variants if v.color}))

        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'variant_id': self.variant_id,
            'size': self.size,
            'color': self.color,
            'quantity': self.quantity,
            'unit_price': unit_price,
            'total_price': round(unit_price * self.quantity, 2),
            'available_stock': stock,
            'is_out_of_stock': is_out_of_stock,
            'exceeds_stock': exceeds_stock,
            'is_low_stock': is_low_stock,
            'available_sizes': sizes,
            'available_colors': colors,
            'product': self.product.to_dict(include_details=False) if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='uq_user_product_wishlist'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    product = db.relationship('Product', lazy='joined')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict(include_details=False) if self.product else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
