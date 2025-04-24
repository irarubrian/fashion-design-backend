from flask import Blueprint, request, jsonify
from app.models import Product, Category
from app.schemas import ProductSchema
from app.extensions import db
from flasgger import swag_from

product_bp = Blueprint('products', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# ---------------------------
# GET /products - List + Pagination
# ---------------------------
@product_bp.route('/products', methods=['GET'])
@swag_from('../swagger_docs/product_list.yml')
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": products.total,
        "pages": products.pages,
        "current_page": products.page,
        "items": products_schema.dump(products.items)
    })

# ---------------------------
# GET /products/<id> - Single Product
# ---------------------------
@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product)

# ---------------------------
# POST /products - Create Product
# ---------------------------
@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = product_schema.load(data)
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

# ---------------------------
# PUT /products/<id> - Update Product
# ---------------------------
@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    updated = product_schema.load(data, instance=product, partial=True)
    db.session.commit()
    return product_schema.jsonify(updated)

# ---------------------------
# DELETE /products/<id> - Delete Product
# ---------------------------
@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 204
