from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="customer")

    cart_items = db.relationship('CartItem', backref='user', cascade='all, delete-orphan', lazy=True)
    orders = db.relationship('Order', backref='user', cascade='all, delete-orphan', lazy=True)
    address = db.relationship('Address', backref='user', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    products = db.relationship('Product', backref='category', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    size = db.Column(db.String(20))
    color = db.Column(db.String(20))
    image_url = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Product', lazy=True)

    def __repr__(self):
        return f"<CartItem User:{self.user_id} Product:{self.product_id}>"

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    invoice = db.relationship('Invoice', backref='order', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Order ID:{self.id} Status:{self.status}>"

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    billing_address = db.Column(db.String(200))
    total_amount = db.Column(db.Float)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Invoice OrderID:{self.order_id}>"

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))

    def __repr__(self):
        return f"<Address {self.street}, {self.city}>"
