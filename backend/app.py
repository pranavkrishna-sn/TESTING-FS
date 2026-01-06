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
ADMIN_TOKENS = {"admin12345"}
PRODUCT_ID_COUNTER = 1

def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health_check() -> Any:
        return jsonify({"status": "ok"}), 200

    @app.route("/products", methods=["POST"])
    def add_product() -> Any:
        nonlocal PRODUCT_ID_COUNTER
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        price = data.get("price")
        description = data.get("description")

        if not name or price is None or not description:
            return jsonify({"error": "Name, price, and description are required"}), 400
        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Price must be a numeric positive value"}), 400
        if name in [p["name"] for p in PRODUCTS.values()]:
            return jsonify({"error": "Product name must be unique"}), 400

        product = {
            "id": PRODUCT_ID_COUNTER,
            "name": name,
            "price": price,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        PRODUCTS[PRODUCT_ID_COUNTER] = product
        app.logger.info("Product '%s' created successfully.", name)
        PRODUCT_ID_COUNTER += 1
        return jsonify({"message": "Product created", "product": product}), 201

    @app.route("/products/<int:product_id>", methods=["PUT"])
    def update_product(product_id: int) -> Any:
        token = request.headers.get("X-Admin-Token")
        if token not in ADMIN_TOKENS:
            app.logger.warning("Unauthorized access attempt for product update.")
            return jsonify({"error": "Unauthorized - Admin access required"}), 403

        data = request.get_json(silent=True) or {}
        product = PRODUCTS.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        name = data.get("name")
        price = data.get("price")
        description = data.get("description")

        if name and name != product["name"]:
            if name in [p["name"] for p in PRODUCTS.values()]:
                return jsonify({"error": "Product name must be unique"}), 400
            product["name"] = name

        if price is not None:
            if not isinstance(price, (int, float)) or price <= 0:
                return jsonify({"error": "Price must be a numeric positive value"}), 400
            product["price"] = price

        if description is not None:
            if description.strip() == "":
                return jsonify({"error": "Description cannot be removed or empty"}), 400
            product["description"] = description

        product["updated_at"] = datetime.utcnow().isoformat()
        PRODUCTS[product_id] = product
        app.logger.info("Product ID %s updated successfully.", product_id)
        return jsonify({"message": "Product updated successfully", "product": product}), 200

    @app.route("/products", methods=["GET"])
    def list_products() -> Any:
        return jsonify(list(PRODUCTS.values())), 200

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Any:
        app.logger.error("Unhandled exception: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=False)