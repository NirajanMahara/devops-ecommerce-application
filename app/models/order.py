from app import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_address = db.Column(db.Text, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'total_amount': self.total_amount,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'shipping_address': self.shipping_address,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at time of purchase
    
    # Relationship
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': self.price,
            'total': self.price * self.quantity
        } 