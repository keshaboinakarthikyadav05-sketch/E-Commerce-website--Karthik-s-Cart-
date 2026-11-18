from datetime import datetime
from . import db

class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    discount_type = db.Column(db.String(20), default='percentage', nullable=False) # 'percentage' or 'fixed'
    discount_value = db.Column(db.Numeric(10, 2), nullable=False)
    min_order_amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    max_discount = db.Column(db.Numeric(10, 2), nullable=True)
    valid_until = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def calculate_discount(self, subtotal):
        if not self.is_active:
            return 0.0
        if self.valid_until and datetime.utcnow() > self.valid_until:
            return 0.0
        if subtotal < float(self.min_order_amount):
            return 0.0

        if self.discount_type == 'percentage':
            disc = (float(self.discount_value) / 100.0) * subtotal
            if self.max_discount and disc > float(self.max_discount):
                disc = float(self.max_discount)
            return round(disc, 2)
        else:
            return round(min(float(self.discount_value), subtotal), 2)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': float(self.discount_value),
            'min_order_amount': float(self.min_order_amount),
            'max_discount': float(self.max_discount) if self.max_discount else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'is_active': self.is_active
        }
