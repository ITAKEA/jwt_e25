from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import users
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('KEY')


jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({'msg': 'Missing email or password'}), 400

    user = users.get(email, None)

    if not user or user['password'] != password:
        return jsonify({'msg': 'Incorrect email or password'}), 401
    
    token = create_access_token(
        identity=email, 
        additional_claims={'role': user['role']} # if you want to work with role based access
        )

    response = make_response(jsonify({'msg': 'You are logged in!'}), 200)
    response.headers['Authorization'] = f'Bearer {token}'
    return response

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    print(get_jwt_identity())
    print(get_jwt())

    return jsonify({
        'logged_in_as': current_user,
        'msg': 'Du har adgang til denne resourse'
    }), 200

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_only():
    claims = get_jwt()
    user_role = claims.get('role', None)

    if user_role != 'admin':
        return jsonify({'msg': 'Access forbidden: insufficient permissions'}), 403

    current_user = get_jwt_identity()
    return jsonify({
        'logged_in_as': current_user,
        'role': user_role,
        'msg': 'Welcome to the admin panel!'
    }), 200

app.run(debug=True)

