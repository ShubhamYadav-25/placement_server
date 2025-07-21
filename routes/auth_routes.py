from flask import Blueprint, request, jsonify
from db.mongo import users_collection

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400

    user = users_collection.find_one({"email": email})
    if user and user.get('password') == password:
        return jsonify({'success': True, 'message': 'Login successful', 'user': {
            'name': user.get('name'), 'email': user.get('email')}})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@auth_routes.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({'success': False, 'message': 'Email already exists'}), 409

    users_collection.insert_one({"name": name, "email": email, "password": password})
    return jsonify({'success': True, 'message': 'User registered successfully'})
