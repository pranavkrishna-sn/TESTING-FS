from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from backend.models.users.user import User
from backend import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400

    new_user = User(email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201