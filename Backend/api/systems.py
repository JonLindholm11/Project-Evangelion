from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel
from typing import Optional
from db.query import systems as system_functions
from db.query import users as user_functions

router = APIRouter(prefix="/api", tags=["systems"])

# Pydantic models for request validation
class CreateSystemRequest(BaseModel):
    system_name: str
    system_img: str

class UpdateSystemRequest(BaseModel):
    system_name: str
    system_img: str

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

# POST /api/systems - Create new system (requires authentication)
@router.post("/systems")
async def create_system(
    system_data: CreateSystemRequest,
    current_user: dict = Depends(get_current_user)
):
    new_system = system_functions.create_system(
        system_data.system_name,
        system_data.system_img
    )
    
    return new_system

# GET /api/systems - Get all systems (requires authentication)
@router.get("/systems")
async def get_all_systems(current_user: dict = Depends(get_current_user)):
    systems = system_functions.get_all_systems()
    return {"systems": systems}

# GET /api/systems/{id} - Get system by ID (requires authentication)
@router.get("/systems/{id}")
async def get_system(id: int, current_user: dict = Depends(get_current_user)):
    system = system_functions.get_system(id)
    
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System not found"
        )
    
    return system

# PUT /api/systems/{id} - Update system (requires authentication)
@router.put("/systems/{id}")
async def update_system(
    id: int,
    system_data: UpdateSystemRequest,
    current_user: dict = Depends(get_current_user)
):
    # Check if system exists
    system = system_functions.get_system(id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System not found"
        )
    
    # Update system
    updated_system = system_functions.update_system(
        id,
        system_data.system_name,
        system_data.system_img
    )
    
    return updated_system

# DELETE /api/systems/{id} - Delete system (requires authentication)
@router.delete("/systems/{id}")
async def delete_system(
    id: int,
    current_user: dict = Depends(get_current_user)
):
    # Check if system exists
    system = system_functions.get_system(id)
    if not system:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System not found"
        )
    
    result = system_functions.delete_system(id)
    return result