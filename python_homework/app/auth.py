import os
import jwt
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv('JWT_SECRET', 'change-me')

def generate_token(user_id: str):
    payload = {'user': user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization header missing or invalid'}), 401
        token = auth_header.split()[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return wrapper