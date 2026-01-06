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

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    session = user_service.validate_user(email, password)
    if session:
        return jsonify({"message": "Login successful", "session_id": session.id}), 200
    
    user = user_service.get_user_by_email(email)
    if user:
        user_service.handle_failed_login(user)
    
    return jsonify({"message": "Invalid email or password"}), 401