from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel
from typing import Optional
from db.query import games as game_functions
from db.query import users as user_functions

router = APIRouter(prefix="/api", tags=["games"])

# Pydantic models for request validation
class CreateGameRequest(BaseModel):
    franchise_id: Optional[int] = None
    system_id: int
    publisher: str
    game_name: str
    game_img: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    description: Optional[str] = None

class UpdateGameRequest(BaseModel):
    franchise_id: Optional[int] = None
    system_id: int
    publisher: str
    game_name: str
    game_img: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    description: Optional[str] = None

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

# POST /api/games - Create new game (requires authentication)
@router.post("/games")
async def create_game(
    game_data: CreateGameRequest,
    current_user: dict = Depends(get_current_user)
):
    new_game = game_functions.create_game(
        game_data.franchise_id,
        game_data.system_id,
        game_data.publisher,
        game_data.game_name,
        game_data.game_img,
        game_data.genre,
        game_data.release_year,
        game_data.description
    )
    
    return new_game

# GET /api/games - Get all games (requires authentication)
@router.get("/games")
async def get_all_games(current_user: dict = Depends(get_current_user)):
    games = game_functions.get_all_games()
    return {"games": games}

# GET /api/games/{id} - Get game by ID (requires authentication)
@router.get("/games/{id}")
async def get_game(id: int, current_user: dict = Depends(get_current_user)):
    game = game_functions.get_game(id)
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return game

# GET /api/games/franchise/{franchise_id} - Get games by franchise (requires authentication)
@router.get("/games/franchise/{franchise_id}")
async def get_games_by_franchise(
    franchise_id: int,
    current_user: dict = Depends(get_current_user)
):
    games = game_functions.get_games_by_franchise(franchise_id)
    return {"games": games}

# GET /api/games/genre/{genre} - Get games by genre (requires authentication)
@router.get("/games/genre/{genre}")
async def get_games_by_genre(
    genre: str,
    current_user: dict = Depends(get_current_user)
):
    games = game_functions.get_games_by_genre(genre)
    return {"games": games}

# PUT /api/games/{id} - Update game (requires authentication)
@router.put("/games/{id}")
async def update_game(
    id: int,
    game_data: UpdateGameRequest,
    current_user: dict = Depends(get_current_user)
):
    # Check if game exists
    game = game_functions.get_game(id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Update game
    updated_game = game_functions.update_game(
        id,
        game_data.franchise_id,
        game_data.system_id,
        game_data.publisher,
        game_data.game_name,
        game_data.game_img,
        game_data.genre,
        game_data.release_year,
        game_data.description
    )
    
    return updated_game

# DELETE /api/games/{id} - Delete game (requires authentication)
@router.delete("/games/{id}")
async def delete_game(
    id: int,
    current_user: dict = Depends(get_current_user)
):
    # Check if game exists
    game = game_functions.get_game(id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    result = game_functions.delete_game(id)
    return result