from app import app
from models import db, User, Category, Product, Address, CartItem, Order, Invoice
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app, db
with app.app_context():
    print("🔄 Seeding database...")

    db.drop_all()
    db.create_all()

    # ------------------- USERS -------------------
    admin = User(
        username="admin",
        email="hamdiaden2424@gmail.com",
        password_hash=generate_password_hash("admin123"),
        role="admin"
    )

    customer = User(
        username="dee",
        email="dee@example.com",
        password_hash=generate_password_hash("password"),
        role="customer"
    )

    db.session.add_all([admin, customer])
    db.session.commit()

    # ------------------- CATEGORIES -------------------
    men = Category(name="Men")
    women = Category(name="Women")
    accessories = Category(name="Accessories")

    db.session.add_all([men, women, accessories])
    db.session.commit()

    # ------------------- PRODUCTS -------------------
    p1 = Product(
        name="Classic T-Shirt",
        description="Comfortable cotton t-shirt",
        price=19.99,
        stock=100,
        size="M",
        color="White",
        image_url="https://example.com/shirt.jpg",
        category_id=men.id
    )
    p2 = Product(
        name="Summer Dress",
        description="Lightweight dress for summer",
        price=39.99,
        stock=50,
        size="S",
        color="Yellow",
        image_url="https://example.com/dress.jpg",
        category_id=women.id
    )
    p3 = Product(
        name="Leather Wallet",
        description="Premium leather wallet",
        price=29.99,
        stock=75,
        size="One Size",
        color="Brown",
        image_url="https://example.com/wallet.jpg",
        category_id=accessories.id
    )

    db.session.add_all([p1, p2, p3])
    db.session.commit()

    # ------------------- ADDRESSES -------------------
    address = Address(
        user_id=customer.id,
        street="123 Main St",
        city="Nairobi",
        state="Nairobi",
        zip_code="00100",
        country="Kenya"
    )
    db.session.add(address)
    db.session.commit()

    # ------------------- CART ITEM -------------------
    cart_item = CartItem(
        user_id=customer.id,
        product_id=p1.id,
        quantity=2
    )
    db.session.add(cart_item)
    db.session.commit()

    # ------------------- ORDER -------------------
    order = Order(
        user_id=customer.id,
        status="paid",
        created_at=datetime.utcnow()
    )
    db.session.add(order)
    db.session.commit()

    # ------------------- INVOICE -------------------
    invoice = Invoice(
        order_id=order.id,
        billing_address=f"{address.street}, {address.city}",
        total_amount=2 * p1.price,
        issued_at=datetime.utcnow()
    )
    db.session.add(invoice)
    db.session.commit()

    print("✅ Seeding complete!")