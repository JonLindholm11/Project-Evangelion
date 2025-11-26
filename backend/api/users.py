from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
import user_functions

router = APIRouter(prefix="/api", tags=["users"])

# Pydantic models for request validation
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUserRequest(BaseModel):
    email: EmailStr
    is_verified: bool

# Dependency to get current user from token
async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    # Expected format: "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    user = user_functions.verify_user_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user

# POST /api/register - Create new user (requires authentication)
@router.post("/register")
async def register(
    user_data: RegisterRequest,
    current_user: dict = Depends(get_current_user)
):
    # Check if user already exists
    existing_user = user_functions.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user (always unverified by default)
    new_user = user_functions.create_user(
        user_data.email,
        user_data.password,
        is_verified=False
    )
    
    # Create token for new user
    token = user_functions.create_token({
        "user_id": new_user['id'],
        "email": new_user['email']
    })
    
    return {
        "token": token,
        "user": {
            "id": new_user['id'],
            "email": new_user['email'],
            "is_verified": new_user['is_verified']
        }
    }

# POST /api/login - Authenticate user
@router.post("/login")
async def login(credentials: LoginRequest):
    result = user_functions.login_user(credentials.email, credentials.password)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["error"]
        )
    
    return result

# GET /api/users - Get all users (requires authentication)
@router.get("/users")
async def get_all_users(current_user: dict = Depends(get_current_user)):
    users = user_functions.get_users()
    return {"users": users}

# GET /api/users/{id} - Get user by ID (requires authentication)
@router.get("/users/{id}")
async def get_user(id: int, current_user: dict = Depends(get_current_user)):
    user = user_functions.get_user(id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

# PUT /api/users/{id} - Update user (requires authentication)
@router.put("/users/{id}")
async def update_user(
    id: int,
    user_data: UpdateUserRequest,
    current_user: dict = Depends(get_current_user)
):
    # Check if user exists
    user = user_functions.get_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user
    updated_user = user_functions.update_user(
        id,
        user_data.email,
        user_data.is_verified
    )
    
    return updated_user

# DELETE /api/users/{id} - Delete user (requires authentication)
@router.delete("/users/{id}")
async def delete_user(
    id: int,
    current_user: dict = Depends(get_current_user)
):
    # Check if user exists
    user = user_functions.get_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    result = user_functions.delete_user(id)
    return result

# GET /api/me - Get current authenticated user
@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user['id'],
        "email": current_user['email'],
        "is_verified": current_user['is_verified']
    }