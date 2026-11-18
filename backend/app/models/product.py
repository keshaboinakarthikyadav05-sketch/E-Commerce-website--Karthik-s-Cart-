from datetime import datetime
import json
from . import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(280), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False, index=True)
    brand = db.Column(db.String(100), nullable=False, index=True)
    original_price = db.Column(db.Numeric(16, 2), nullable=False)
    discounted_price = db.Column(db.Numeric(16, 2), nullable=False)
    discount_percent = db.Column(db.Integer, default=0, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    rating = db.Column(db.Numeric(3, 2), default=4.5, nullable=False)
    num_reviews = db.Column(db.Integer, default=0, nullable=False)
    specifications = db.Column(db.JSON, nullable=True)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_trending = db.Column(db.Boolean, default=False, nullable=False)
    is_bestseller = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy='joined', cascade='all, delete-orphan', order_by='ProductImage.display_order')
    variants = db.relationship('ProductVariant', backref='product', lazy='joined', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_details=True):
        primary_img = None
        all_imgs = []
        for img in self.images:
            all_imgs.append(img.to_dict())
            if img.is_primary and not primary_img:
                primary_img = img.image_url
        
        if not primary_img and all_imgs:
            primary_img = all_imgs[0]['image_url']
            
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else '',
            'category_slug': self.category.slug if self.category else '',
            'brand': self.brand,
            'original_price': float(self.original_price),
            'discounted_price': float(self.discounted_price),
            'discount_percent': self.discount_percent,
            'stock': self.stock,
            'rating': float(self.rating) if self.rating else 0.0,
            'num_reviews': self.num_reviews,
            'primary_image': primary_img or 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80',
            'is_featured': self.is_featured,
            'is_trending': self.is_trending,
            'is_bestseller': self.is_bestseller,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_details:
            data['images'] = all_imgs
            data['variants'] = [v.to_dict() for v in self.variants]
            data['specifications'] = self.specifications or {}
            
            # Available unique sizes and colors extracted from variants
            sizes = sorted(list({v.size for v in self.variants if v.size}))
            colors = sorted(list({v.color for v in self.variants if v.color}))
            data['available_sizes'] = sizes
            data['available_colors'] = colors

        return data

class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'is_primary': self.is_primary,
            'display_order': self.display_order
        }

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    size = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    sku = db.Column(db.String(100), nullable=True)
    additional_price = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    stock = db.Column(db.Integer, default=10, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'size': self.size,
            'color': self.color,
            'sku': self.sku,
            'additional_price': float(self.additional_price),
            'stock': self.stock
        }
