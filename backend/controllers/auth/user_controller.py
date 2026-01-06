from flask import Blueprint, request, jsonify
from backend.services.auth.user_service import UserService

user_bp = Blueprint('user', __name__)
user_service = UserService()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if user_service.register_user(email, password):
        return jsonify({"message": "User registered successfully"}), 201
    return jsonify({"message": "User registration failed"}), 400