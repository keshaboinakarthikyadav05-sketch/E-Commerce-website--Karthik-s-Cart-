from datetime import datetime
from . import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, index=True)
    razorpay_order_id = db.Column(db.String(100), nullable=True, index=True)
    razorpay_payment_id = db.Column(db.String(100), nullable=True, index=True)
    razorpay_signature = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default='INR', nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False) # pending, captured, failed, refunded
    method = db.Column(db.String(50), default='razorpay', nullable=False) # razorpay, cod
    error_code = db.Column(db.String(100), nullable=True)
    error_description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'razorpay_order_id': self.razorpay_order_id,
            'razorpay_payment_id': self.razorpay_payment_id,
            'amount': float(self.amount),
            'currency': self.currency,
            'status': self.status,
            'method': self.method,
            'error_code': self.error_code,
            'error_description': self.error_description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
