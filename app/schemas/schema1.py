from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import User, Category, Product, Order, OrderItem, CartItem

# ---------- USER ----------
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)

class UserCreateSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

# ---------- CATEGORY ----------
class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

class CategoryCreateSchema(Schema):
    name = fields.Str(required=True)

# ---------- PRODUCT ----------
class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        load_instance = True

class ProductCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float(required=True)
    stock = fields.Int(missing=0)
    category_id = fields.Int(required=True)

# ---------- CART ITEM ----------
class CartItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        include_fk = True
        load_instance = True

class CartItemCreateSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

# ---------- ORDER ----------
class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
        load_instance = True

# ---------- ORDER ITEM ----------
class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        include_fk = True
        load_instance = True
