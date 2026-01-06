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

        if not name or not description or price is None:
            return jsonify({"error": "Name, description and price are required"}), 400
        if name in [p["name"] for p in PRODUCTS.values() if not p["deleted"]]:
            return jsonify({"error": "Product name must be unique"}), 400
        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Invalid price"}), 400

        PRODUCTS[PRODUCT_ID_COUNTER] = {
            "id": PRODUCT_ID_COUNTER,
            "name": name,
            "price": price,
            "description": description,
            "deleted": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        app.logger.info("Product '%s' created successfully.", name)
        PRODUCT_ID_COUNTER += 1
        return jsonify({"message": "Product created"}), 201

    @app.route("/products/<int:product_id>/delete", methods=["DELETE"])
    def delete_product(product_id: int) -> Any:
        token = request.headers.get("X-Admin-Token")
        confirm = request.args.get("confirm", "false").lower()

        if token not in ADMIN_TOKENS:
            app.logger.warning("Unauthorized delete attempt.")
            return jsonify({"error": "Unauthorized - Admin access required"}), 403
        if confirm != "true":
            return jsonify({"error": "Confirmation required"}), 400

        product = PRODUCTS.get(product_id)
        if not product or product["deleted"]:
            app.logger.warning("Product not found or already deleted, ID: %s", product_id)
            return jsonify({"error": "Product not found"}), 404

        product["deleted"] = True
        product["updated_at"] = datetime.utcnow().isoformat()
        PRODUCTS[product_id] = product
        app.logger.info("Product %s marked as deleted.", product["name"])
        return jsonify({"message": f"Product '{product['name']}' deleted successfully"}), 200

    @app.route("/products", methods=["GET"])
    def list_products() -> Any:
        visible_products = [p for p in PRODUCTS.values() if not p["deleted"]]
        return jsonify(visible_products), 200

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Any:
        app.logger.error("Unhandled exception: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=False)