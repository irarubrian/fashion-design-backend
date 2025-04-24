from flask import Blueprint, request, jsonify
from app.models import Category
from app.schemas import CategorySchema
from app.extensions import db
from flasgger import swag_from

category_bp = Blueprint('categories', __name__)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

# ---------------------------
# GET /categories - List + Pagination
# ---------------------------
@category_bp.route('/categories', methods=['GET'])
@swag_from('../swagger_docs/category_list.yml')
def get_categories():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    categories = Category.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": categories.total,
        "pages": categories.pages,
        "current_page": categories.page,
        "items": categories_schema.dump(categories.items)
    })

# ---------------------------
# GET /categories/<id> - Get Single Category
# ---------------------------
@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return category_schema.jsonify(category)

# ---------------------------
# POST /categories - Create Category
# ---------------------------
@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category = category_schema.load(data)
    db.session.add(category)
    db.session.commit()
    return category_schema.jsonify(category), 201

# ---------------------------
# PUT /categories/<id> - Update Category
# ---------------------------
@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    updated = category_schema.load(data, instance=category, partial=True)
    db.session.commit()
    return category_schema.jsonify(updated)

# ---------------------------
# DELETE /categories/<id> - Delete Category
# ---------------------------
@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 204
