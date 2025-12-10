from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from db.query import playedGames as played_games_functions
from db.query import games as game_functions

router = APIRouter(prefix="/api/played", tags=["played_games"])

# Pydantic models
class PlayedGameCreate(BaseModel):
    game_id: int
    rating: Optional[int] = None
    notes: Optional[str] = None

class PlayedGameUpdate(BaseModel):
    rating: Optional[int] = None
    notes: Optional[str] = None

# GET - Get all played games for a user
@router.get("/{user_id}")
def get_played_games(user_id: int):
    """Get all games a user has played"""
    played_games = played_games_functions.get_user_played_games(user_id)
    return {"played_games": played_games}

# POST - Mark game as played
@router.post("/{user_id}")
def mark_as_played(user_id: int, played_game: PlayedGameCreate):
    """Mark a game as played for a user"""
    
    # Check if already played
    if played_games_functions.check_if_played(user_id, played_game.game_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game already marked as played"
        )
    
    # Check if game exists
    game = game_functions.get_game(played_game.game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Create new played game entry
    result = played_games_functions.mark_game_as_played(
        user_id,
        played_game.game_id,
        played_game.rating,
        played_game.notes
    )
    
    return {"message": "Game marked as played", "data": result}

# DELETE - Remove from played games
@router.delete("/{user_id}/{game_id}")
def unmark_as_played(user_id: int, game_id: int):
    """Remove a game from user's played list"""
    
    # Check if it exists
    if not played_games_functions.check_if_played(user_id, game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Played game record not found"
        )
    
    result = played_games_functions.unmark_game_as_played(user_id, game_id)
    return result

# PATCH - Update rating/notes
@router.patch("/{user_id}/{game_id}")
def update_played_game(
    user_id: int,
    game_id: int,
    update_data: PlayedGameUpdate
):
    """Update rating or notes for a played game"""
    
    # Check if it exists
    if not played_games_functions.check_if_played(user_id, game_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Played game record not found"
        )
    
    # Validate rating
    if update_data.rating is not None:
        if update_data.rating < 1 or update_data.rating > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be 1-5"
            )
    
    result = played_games_functions.update_played_game(
        user_id,
        game_id,
        update_data.rating,
        update_data.notes
    )
    
    return result

# GET - Check if game is played
@router.get("/{user_id}/check/{game_id}")
def check_if_played(user_id: int, game_id: int):
    """Check if user has played a specific game"""
    
    is_played = played_games_functions.check_if_played(user_id, game_id)
    return {"played": is_played}