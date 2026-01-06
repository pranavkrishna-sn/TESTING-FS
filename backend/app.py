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

USER_PROFILES: dict[str, dict[str, Any]] = {}

def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health_check() -> Any:
        return jsonify({"status": "ok"}), 200

    @app.route("/profile/<string:email>", methods=["GET"])
    def get_profile(email: str) -> Any:
        profile = USER_PROFILES.get(email)
        if not profile:
            app.logger.warning("Profile not found for %s", email)
            return jsonify({"error": "Profile not found"}), 404
        return jsonify(profile), 200

    @app.route("/profile/<string:email>", methods=["PUT"])
    def update_profile(email: str) -> Any:
        data = request.get_json(silent=True) or {}
        if not data:
            app.logger.warning("Update request missing data for %s", email)
            return jsonify({"error": "No update data provided"}), 400

        current = USER_PROFILES.get(email)
        if not current:
            current = {
                "email": email,
                "name": "",
                "preferences": {},
                "updated_at": datetime.utcnow().isoformat()
            }

        for key, value in data.items():
            if key != "email":
                current[key] = value
        current["updated_at"] = datetime.utcnow().isoformat()
        USER_PROFILES[email] = current
        app.logger.info("Profile updated successfully for %s", email)
        return jsonify({"message": "Profile updated", "profile": current}), 200

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Any:
        app.logger.error("Unhandled exception: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=False)