import logging
import sys
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

PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "attributes": {"color": "black", "brand": "TechPro"},
        "description": "Ergonomic wireless mouse",
    },
    {
        "id": 2,
        "name": "Bluetooth Headphones",
        "category": "Electronics",
        "attributes": {"color": "white", "brand": "SoundBeat"},
        "description": "Noise-cancelling Bluetooth headphones",
    },
    {
        "id": 3,
        "name": "Office Chair",
        "category": "Furniture",
        "attributes": {"color": "blue", "material": "fabric"},
        "description": "Comfortable ergonomic office chair",
    }
]

PAGE_SIZE_DEFAULT = 2

def highlight_term(text: str, term: str) -> str:
    lower_text, lower_term = text.lower(), term.lower()
    if lower_term in lower_text:
        start = lower_text.index(lower_term)
        end = start + len(term)
        return text[:start] + "[" + text[start:end] + "]" + text[end:]
    return text

def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health_check() -> Any:
        return jsonify({"status": "ok"}), 200

    @app.route("/products/search", methods=["GET"])
    def search_products() -> Any:
        query = request.args.get("query", "").strip()
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", PAGE_SIZE_DEFAULT))

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        filtered = []
        for product in PRODUCTS:
            match_fields = [
                product["name"].lower(),
                product["category"].lower(),
                " ".join(str(v).lower() for v in product["attributes"].values()),
            ]
            if any(query.lower() in field for field in match_fields):
                highlighted_name = highlight_term(product["name"], query)
                highlighted_description = highlight_term(product["description"], query)
                filtered.append({
                    **product,
                    "name": highlighted_name,
                    "description": highlighted_description,
                })

        total = len(filtered)
        start_index = (page - 1) * size
        end_index = start_index + size
        paginated = filtered[start_index:end_index]

        app.logger.info("Search executed for query '%s' returning %d/%d results.", query, len(paginated), total)
        return jsonify({
            "query": query,
            "page": page,
            "page_size": size,
            "total_results": total,
            "results": paginated,
        }), 200

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Any:
        app.logger.error("Unhandled exception: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=False)