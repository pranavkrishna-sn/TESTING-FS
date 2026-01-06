from flask import Blueprint, request, jsonify
from backend.services.products.product_service import ProductService

product_bp = Blueprint('product', __name__)
product_service = ProductService()

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    category = data.get('category')

    if not all([name, price, description]):
        return jsonify({"message": "Name, price, and description are required"}), 400

    existing_product = product_service.get_product_by_name(name)
    if existing_product:
        return jsonify({"message": "Product with this name already exists"}), 400

    product = product_service.add_product(name, price, description, category)
    return jsonify({"message": "Product added successfully", "product_id": product.id}), 201

@product_bp.route('/update', methods=['POST'])
def update_product():
    data = request.json
    product_id = data.get('id')
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    category = data.get('category')

    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400

    if price is not None and not isinstance(price, (float, int)):
        return jsonify({"message": "Price must be a numeric value"}), 400

    success = product_service.update_product(product_id, name, price, description, category)
    if success:
        return jsonify({"message": "Product updated successfully"}), 200
    return jsonify({"message": "Product not found"}), 404