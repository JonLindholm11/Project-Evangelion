import jwt
import os
from datetime import datetime, timedelta

SECRET = os.getenv("JWT_SECRET")

def create_token(payload):
    """Creates a token with the given payload"""
    return jwt.encode(
        {
            **payload,
            "exp": datetime.utcnow() + timedelta(days=7)
        },
        SECRET,
        algorithm="HS256"
    )

def verify_token(token):
    """Extracts the payload from a token"""
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None