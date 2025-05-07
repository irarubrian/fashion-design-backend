from datetime import datetime
from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='M-PESA')
    payment_status = db.Column(db.String(20), default='Pending')  # Pending, Paid, Failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.id} - Status: {self.payment_status}>'
