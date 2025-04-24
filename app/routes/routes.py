from flask import Blueprint, request, jsonify
from app.models import Product, Category
from app.schemas import ProductSchema, CategorySchema
from app.extensions import db
from flasgger.utils import swag_from

api_bp = Blueprint('api', __name__)
product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)
category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)


@api_bp.route('/products', methods=['GET'])
@swag_from('swagger_docs/product_list.yml')
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page,
        'items': product_list_schema.dump(products.items)
    })


@api_bp.route('/categories', methods=['GET'])
@swag_from('swagger_docs/category_list.yml')
def get_categories():
    categories = Category.query.all()
    return jsonify(category_list_schema.dump(categories))
