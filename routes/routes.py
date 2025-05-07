from flask import Blueprint, request, jsonify
from models.models import User, Product, Category, CartItem, Order, Invoice, Address
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db      

main = Blueprint("main", __name__)


@main.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400
    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role=data.get("role", "customer")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@main.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password_hash, data["password"]):
        return jsonify({"message": "Login successful", "user": {"id": user.id, "role": user.role}})
    return jsonify({"error": "Invalid credentials"}), 401

@main.route("/products", methods=["GET"])
def get_all_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image_url": p.image_url,
            "category": p.category.name if p.category else None
        } for p in products
    ])

@main.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

@main.route("/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": item.id,
            "product": item.product.name,
            "quantity": item.quantity,
            "subtotal": item.quantity * item.product.price
        } for item in items
    ])

@main.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.json
    item = CartItem(
        user_id=data["user_id"],
        product_id=data["product_id"],
        quantity=data["quantity"]
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item added to cart"})

@main.route("/orders/<int:user_id>", methods=["GET"])
def get_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": o.id,
            "status": o.status,
            "invoice": {
                "billing_address": o.invoice.billing_address,
                "total": o.invoice.total_amount
            } if o.invoice else None
        } for o in orders
    ])

@main.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    user_id = data["user_id"]
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    order = Order(user_id=user_id, status="paid")
    db.session.add(order)
    db.session.flush()

    total = sum([item.quantity * item.product.price for item in cart_items])
    address = Address.query.filter_by(user_id=user_id).first()
    billing = f"{address.street}, {address.city}" if address else "No address"

    invoice = Invoice(
        order_id=order.id,
        billing_address=billing,
        total_amount=total,
        issued_at=datetime.utcnow()
    )
    db.session.add(invoice)

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()
    return jsonify({"message": "Checkout successful", "order_id": order.id})

@main.route("/admin/products", methods=["POST"])
def create_product():
    data = request.json
    product = Product(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        stock=data["stock"],
        size=data["size"],
        color=data["color"],
        image_url=data.get("image_url", ""),
        category_id=data["category_id"]
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created"})

@main.route("/admin/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.json
    for key in ["name", "description", "price", "stock", "size", "color", "image_url", "category_id"]:
        setattr(product, key, data.get(key, getattr(product, key)))

    db.session.commit()
    return jsonify({"message": "Product updated"})

@main.route("/admin/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})
