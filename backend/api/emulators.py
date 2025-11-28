from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel
from typing import Optional
import emulator_functions
import user_functions

router = APIRouter(prefix="/api", tags=["emulators"])

# Pydantic models for request validation
class CreateEmulatorRequest(BaseModel):
    system_id: int
    emulator_name: str
    emulator_file: str
    emulator_img: str

class UpdateEmulatorRequest(BaseModel):
    system_id: int
    emulator_name: str
    emulator_file: str
    emulator_img: str

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

# POST /api/emulators - Create new emulator (requires authentication)
@router.post("/emulators")
async def create_emulator(
    emulator_data: CreateEmulatorRequest,
    current_user: dict = Depends(get_current_user)
):
    new_emulator = emulator_functions.create_emulator(
        emulator_data.system_id,
        emulator_data.emulator_name,
        emulator_data.emulator_file,
        emulator_data.emulator_img
    )
    
    return new_emulator

# GET /api/emulators - Get all emulators (requires authentication)
@router.get("/emulators")
async def get_all_emulators(current_user: dict = Depends(get_current_user)):
    emulators = emulator_functions.get_all_emulators()
    return {"emulators": emulators}

# GET /api/emulators/{id} - Get emulator by ID (requires authentication)
@router.get("/emulators/{id}")
async def get_emulator(id: int, current_user: dict = Depends(get_current_user)):
    emulator = emulator_functions.get_emulator(id)
    
    if not emulator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emulator not found"
        )
    
    return emulator

# PUT /api/emulators/{id} - Update emulator (requires authentication)
@router.put("/emulators/{id}")
async def update_emulator(
    id: int,
    emulator_data: UpdateEmulatorRequest,
    current_user: dict = Depends(get_current_user)
):
    # Check if emulator exists
    emulator = emulator_functions.get_emulator(id)
    if not emulator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emulator not found"
        )
    
    # Update emulator
    updated_emulator = emulator_functions.update_emulator(
        id,
        emulator_data.system_id,
        emulator_data.emulator_name,
        emulator_data.emulator_file,
        emulator_data.emulator_img
    )
    
    return updated_emulator

# DELETE /api/emulators/{id} - Delete emulator (requires authentication)
@router.delete("/emulators/{id}")
async def delete_emulator(
    id: int,
    current_user: dict = Depends(get_current_user)
):
    # Check if emulator exists
    emulator = emulator_functions.get_emulator(id)
    if not emulator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emulator not found"
        )
    
    result = emulator_functions.delete_emulator(id)
    return result