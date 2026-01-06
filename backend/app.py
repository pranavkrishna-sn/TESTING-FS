import logging
import sys
import secrets
from datetime import datetime, timedelta
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

PASSWORD_RESET_TOKENS: dict[str, dict[str, Any]] = {}
TOKEN_EXPIRATION_HOURS = 24

def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health_check() -> Any:
        return jsonify({"status": "ok"}), 200

    @app.route("/password-reset/request", methods=["POST"])
    def request_password_reset() -> Any:
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        if not email:
            app.logger.warning("Password reset request missing email field.")
            return jsonify({"error": "Email is required"}), 400

        token = secrets.token_urlsafe(32)
        PASSWORD_RESET_TOKENS[email] = {
            "token": token,
            "expires_at": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
            "verified": False
        }

        app.logger.info("Password reset token generated for email %s", email)
        # In a real system, send email here via integration
        return jsonify({
            "message": "Password reset link sent to registered email",
            "token": token
        }), 200

    @app.route("/password-reset/verify", methods=["POST"])
    def verify_reset_token() -> Any:
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        token = data.get("token")

        info = PASSWORD_RESET_TOKENS.get(email)
        if not info or info["token"] != token:
            app.logger.warning("Invalid or missing reset token during verification.")
            return jsonify({"error": "Invalid token"}), 400

        if datetime.utcnow() > info["expires_at"]:
            del PASSWORD_RESET_TOKENS[email]
            app.logger.warning("Expired reset token for email %s", email)
            return jsonify({"error": "Token expired"}), 403

        info["verified"] = True
        app.logger.info("Password reset token verified successfully for email %s", email)
        return jsonify({"message": "Token verified successfully"}), 200

    @app.route("/password-reset/confirm", methods=["POST"])
    def confirm_password_reset() -> Any:
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        new_password = data.get("new_password")

        info = PASSWORD_RESET_TOKENS.get(email)
        if not info or not info.get("verified"):
            return jsonify({"error": "Reset verification required"}), 400

        if datetime.utcnow() > info["expires_at"]:
            del PASSWORD_RESET_TOKENS[email]
            app.logger.warning("Attempted password reset after token expiration for %s", email)
            return jsonify({"error": "Token expired"}), 403

        if not new_password or len(new_password) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400

        del PASSWORD_RESET_TOKENS[email]
        app.logger.info("Password reset successful for email %s", email)
        return jsonify({"message": "Password has been reset successfully"}), 200

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> Any:
        app.logger.error("Unhandled exception: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=False)