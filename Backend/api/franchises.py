from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel
from typing import Optional
import franchise_functions
import user_functions

router = APIRouter(prefix="/api", tags=["franchises"])

# Pydantic models for request validation
class CreateFranchiseRequest(BaseModel):
    system_id: int
    franchise_name: str
    franchise_img: str

class UpdateFranchiseRequest(BaseModel):
    system_id: int
    franchise_name: str
    franchise_img: str

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

# POST /api/franchises - Create new franchise (requires authentication)
@router.post("/franchises")
async def create_franchise(
    franchise_data: CreateFranchiseRequest,
    current_user: dict = Depends(get_current_user)
):
    new_franchise = franchise_functions.create_franchise(
        franchise_data.system_id,
        franchise_data.franchise_name,
        franchise_data.franchise_img
    )
    
    return new_franchise

# GET /api/franchises - Get all franchises (requires authentication)
@router.get("/franchises")
async def get_all_franchises(current_user: dict = Depends(get_current_user)):
    franchises = franchise_functions.get_all_franchises()
    return {"franchises": franchises}

# GET /api/franchises/{id} - Get franchise by ID (requires authentication)
@router.get("/franchises/{id}")
async def get_franchise(id: int, current_user: dict = Depends(get_current_user)):
    franchise = franchise_functions.get_franchise(id)
    
    if not franchise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Franchise not found"
        )
    
    return franchise

# PUT /api/franchises/{id} - Update franchise (requires authentication)
@router.put("/franchises/{id}")
async def update_franchise(
    id: int,
    franchise_data: UpdateFranchiseRequest,
    current_user: dict = Depends(get_current_user)
):
    # Check if franchise exists
    franchise = franchise_functions.get_franchise(id)
    if not franchise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Franchise not found"
        )
    
    # Update franchise
    updated_franchise = franchise_functions.update_franchise(
        id,
        franchise_data.system_id,
        franchise_data.franchise_name,
        franchise_data.franchise_img
    )
    
    return updated_franchise

# DELETE /api/franchises/{id} - Delete franchise (requires authentication)
@router.delete("/franchises/{id}")
async def delete_franchise(
    id: int,
    current_user: dict = Depends(get_current_user)
):
    # Check if franchise exists
    franchise = franchise_functions.get_franchise(id)
    if not franchise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Franchise not found"
        )
    
    result = franchise_functions.delete_franchise(id)
    return result