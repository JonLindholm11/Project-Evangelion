import bcrypt
from db.client import fetch_all, fetch_one, execute_query
from db.utils.jwt_utils import create_token, verify_token

def create_user(email, password, is_verified):
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    SQL = """
        INSERT INTO users (email, password_hash, is_verified)
        VALUES (?, ?, ?)
    """
    
    user_id = execute_query(SQL, [email, hashed_password, is_verified])
    return get_user(user_id)

def get_users():
    SQL = """
        SELECT *
        FROM users
    """
    return fetch_all(SQL)

def get_user(id):
    SQL = """
        SELECT *
        FROM users
        WHERE id = ?
    """
    return fetch_one(SQL, [id])

def get_user_by_email(email):
    """Get user by email"""
    SQL = """
        SELECT *
        FROM users
        WHERE email = ?
    """
    return fetch_one(SQL, [email])

def update_user(id, email, is_verified):
    SQL = """
        UPDATE users
        SET
            email = ?,
            is_verified = ?
        WHERE id = ?
    """
    execute_query(SQL, [email, is_verified, id])
    return get_user(id)

def delete_user(user_id):
    SQL = """
        DELETE FROM users
        WHERE id = ?
    """
    execute_query(SQL, [user_id])
    return {"message": "User deleted"}

def login_user(email, password):
    """Authenticate user and return token"""
    user = get_user_by_email(email)
    
    if not user:
        return {"error": "Invalid email or password"}
    

    if not user['is_verified']:
        return {"error": "Account not verified"}
    

    if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):

        token = create_token({
            "user_id": user['id'],
            "email": user['email']
        })
        

        return {
            "token": token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "is_verified": user['is_verified']
            }
        }
    
    return {"error": "Invalid email or password"}

def verify_user_token(token):
    """Verify JWT token and return user data"""
    payload = verify_token(token)
    
    if not payload:
        return None
    

    return get_user(payload['user_id'])