from flask import Blueprint, request, jsonify
from models.models import Product, Category, CartItem, Order, Invoice, Address
from datetime import datetime
from extensions import db

main = Blueprint("main", __name__)


# ======================
# PRODUCTS
# ======================
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


# ======================
# CATEGORIES
# ======================
@main.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])


# ======================
# CART
# ======================
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
    data = request.get_json()

    item = CartItem(
        user_id=data["user_id"],
        product_id=data["product_id"],
        quantity=data.get("quantity", 1)
    )
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Item added to cart"}), 201


# ======================
# ORDERS
# ======================
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


# ======================
# CHECKOUT
# ======================
@main.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    user_id = data["user_id"]

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    order = Order(user_id=user_id, status="paid")
    db.session.add(order)
    db.session.flush()  # get order.id

    total = sum(item.quantity * item.product.price for item in cart_items)
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

    return jsonify({
        "message": "Checkout successful",
        "order_id": order.id
    }), 201


# ======================
# ADMIN – PRODUCTS
# ======================
@main.route("/admin/products", methods=["POST"])
def create_product():
    data = request.get_json()

    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        stock=data.get("stock", 0),
        size=data.get("size"),
        color=data.get("color"),
        image_url=data.get("image_url", ""),
        category_id=data["category_id"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product created"}), 201


@main.route("/admin/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    for key in ["name", "description", "price", "stock", "size", "color", "image_url", "category_id"]:
        if key in data:
            setattr(product, key, data[key])

    db.session.commit()
    return jsonify({"message": "Product updated"})


@main.route("/admin/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})
