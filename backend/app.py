import logging
import sys
from datetime import datetime
from typing import Any
from flask import Flask, jsonify, request
from logging.config import dictConfig

def configure_logging() -> None:
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["wsgi"]
        }
    })

PRODUCTS: dict[int, dict[str, Any]] = {}
CATEGORIES: dict[int, str] = {}
PRODUCT_ID_COUNTER = 1

def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health_check() -> Any:
        return jsonify({"status": "ok"}), 200

    @app.route("/categories", methods=["POST"])
    def add_category() -> Any:
        nonlocal CATEGORIES
        data = request.get_json(silent=True) or {}
        category_name = data.get("name")
        if not category_name:
            return jsonify({"error": "Category name is required"}), 400
        if category_name in CATEGORIES.values():
            return jsonify({"error": "Category already exists"}), 400
        category_id = len(CATEGORIES) + 1
        CATEGORIES[category_id] = category_name
        app.logger.info("Category '%s' created successfully.", category_name)
        return jsonify({"message": "Category created", "id": category_id, "name": category_name}), 201

    @app.route("/products", methods=["POST"])
    def add_product() -> Any:
        nonlocal PRODUCTS, PRODUCT_ID_COUNTER
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        price = data.get("price")
        description = data.get("description")
        category_id = data.get("category_id")

        if not name or not description or price is None or category_id is None:
            return jsonify({"error": "Name, price, description, and category_id are required"}), 400

        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Price must be a positive number"}), 400

        if name in [p["name"] for p in PRODUCTS.values()]:
            return jsonify({"error": "Product name must be unique"}), 400

        if category_id not in CATEGORIES:
            return jsonify({"error": "Invalid category"}), 400

        product = {
            "id": PRODUCT_ID_COUNTER,
            "name": name,
            "price": price,
            "description": description,
            "category_id": category_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        PRODUCTS[PRODUCT_ID_COUNTER] = product
        PRODUCT_ID_COUNTER += 1
        app.logger.info("Product '%s' added successfully.", name)
        return jsonify({"message": "Product added", "product": product}), 201

    @app.route("/products", methods=["GET"])
    def list_products() -> Any:
        all_products = list(PRODUCTS.values())
        return jsonify(all_products), 200

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Any:
        app.logger.error("Unhandled exception: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=False)