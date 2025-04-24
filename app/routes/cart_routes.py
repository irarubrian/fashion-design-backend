from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import CartItem, Product
from app.extensions import db
from app.schemas import CartItemSchema
from flasgger import swag_from

cart_bp = Blueprint('cart', __name__)
cart_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

# -------------------------------
# GET /cart - Get User's Cart
# -------------------------------
@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
@swag_from('../swagger_docs/cart_get.yml')
def get_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify(cart_items_schema.dump(cart_items))

# -------------------------------
# POST /cart - Add Item to Cart
# -------------------------------
@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
@swag_from('../swagger_docs/cart_add.yml')
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({"error": "Not enough stock"}), 400

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return cart_schema.jsonify(cart_item), 201

# -------------------------------
# PUT /cart/<int:item_id> - Update Quantity
# -------------------------------
@cart_bp.route('/cart/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.get_or_404(item_id)

    if cart_item.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    quantity = data.get('quantity')

    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity

    db.session.commit()
    return cart_schema.jsonify(cart_item)

# -------------------------------
# DELETE /cart/<int:item_id>
# -------------------------------
@cart_bp.route('/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.get_or_404(item_id)

    if cart_item.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Item removed"}), 204
