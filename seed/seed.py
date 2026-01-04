from app import app
from extensions import db
from models import (
    User,
    Category,
    Product,
    Address,
    CartItem,
    Order,
    Invoice,
)
from werkzeug.security import generate_password_hash
from datetime import datetime


def seed():
    with app.app_context():
        print("🔄 Seeding database...")

        # ------------------- USERS -------------------
        admin = User.query.filter_by(email="admin@example.com").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=generate_password_hash("admin123"),
                role="admin",
            )
            db.session.add(admin)

        customer = User.query.filter_by(email="dee@example.com").first()
        if not customer:
            customer = User(
                username="dee",
                email="dee@example.com",
                password_hash=generate_password_hash("password"),
                role="customer",
            )
            db.session.add(customer)

        db.session.commit()

        # ------------------- CATEGORIES -------------------
        def get_or_create_category(name):
            category = Category.query.filter_by(name=name).first()
            if not category:
                category = Category(name=name)
                db.session.add(category)
                db.session.commit()
            return category

        men = get_or_create_category("Men")
        women = get_or_create_category("Women")
        accessories = get_or_create_category("Accessories")

        # ------------------- PRODUCTS -------------------
        if not Product.query.first():
            products = [
                Product(
                    name="Classic T-Shirt",
                    description="Comfortable cotton t-shirt",
                    price=19.99,
                    stock=100,
                    size="M",
                    color="White",
                    image_url="https://example.com/shirt.jpg",
                    category_id=men.id,
                ),
                Product(
                    name="Summer Dress",
                    description="Lightweight dress for summer",
                    price=39.99,
                    stock=50,
                    size="S",
                    color="Yellow",
                    image_url="https://example.com/dress.jpg",
                    category_id=women.id,
                ),
                Product(
                    name="Leather Wallet",
                    description="Premium leather wallet",
                    price=29.99,
                    stock=75,
                    size="One Size",
                    color="Brown",
                    image_url="https://example.com/wallet.jpg",
                    category_id=accessories.id,
                ),
            ]
            db.session.add_all(products)
            db.session.commit()

        # ------------------- ADDRESS -------------------
        if not Address.query.filter_by(user_id=customer.id).first():
            address = Address(
                user_id=customer.id,
                street="123 Main St",
                city="Nairobi",
            )
            db.session.add(address)
            db.session.commit()
        else:
            address = Address.query.filter_by(user_id=customer.id).first()

        # ------------------- CART ITEM -------------------
        if not CartItem.query.filter_by(user_id=customer.id).first():
            product = Product.query.first()
            cart_item = CartItem(
                user_id=customer.id,
                product_id=product.id,
                quantity=2,
            )
            db.session.add(cart_item)
            db.session.commit()

        # ------------------- ORDER + INVOICE -------------------
        if not Order.query.filter_by(user_id=customer.id).first():
            product = Product.query.first()
            order = Order(
                user_id=customer.id,
                status="paid",
                created_at=datetime.utcnow(),
            )
            db.session.add(order)
            db.session.commit()

            invoice = Invoice(
                order_id=order.id,
                billing_address=f"{address.street}, {address.city}",
                total_amount=2 * product.price,
                issued_at=datetime.utcnow(),
            )
            db.session.add(invoice)
            db.session.commit()

        print("✅ Seeding complete!")


if __name__ == "__main__":
    seed()
