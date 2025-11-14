from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
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

    return jsonify({'msg': 'You are logged in!'}), 200


app.run(debug=True)

