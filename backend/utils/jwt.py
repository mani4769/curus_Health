import jwt
import os
from datetime import datetime, timedelta

def encode_auth_token(user_id, role):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'role': role
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    except Exception as e:
        return None

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
