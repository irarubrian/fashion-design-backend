from extensions import db
from datetime import datetime


# ======================
# USER
# ======================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="customer", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship(
        "CartItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    orders = db.relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    address = db.relationship(
        "Address",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"


# ======================
# CATEGORY
# ======================
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    products = db.relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


# ======================
# PRODUCT
# ======================
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    size = db.Column(db.String(20))
    color = db.Column(db.String(20))
    image_url = db.Column(db.String(200))

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False
    )

    category = db.relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name}>"


# ======================
# CART ITEM
# ======================
class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )

    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="cart_items")
    product = db.relationship("Product")

    def __repr__(self):
        return f"<CartItem user={self.user_id} product={self.product_id}>"


# ======================
# ORDER
# ======================
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(50), default="M-PESA")
    status = db.Column(db.String(20), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    user = db.relationship("User", back_populates="orders")

    invoice = db.relationship(
        "Invoice",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Order id={self.id} status={self.status}>"


# ======================
# INVOICE
# ======================
class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    billing_address = db.Column(db.String(200))
    total_amount = db.Column(db.Float, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship("Order", back_populates="invoice")

    def __repr__(self):
        return f"<Invoice order_id={self.order_id}>"


# ======================
# ADDRESS
# ======================
class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="address")

    def __repr__(self):
        return f"<Address {self.street}, {self.city}>"
