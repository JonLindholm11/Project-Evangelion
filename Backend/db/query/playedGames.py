from db.client import fetch_all, fetch_one, execute_query

def get_user_played_games(user_id):
    """Get all games a user has played"""
    SQL = """
        SELECT 
            pg.*,
            g.game_name,
            g.genre,
            g.game_img
        FROM played_games pg
        JOIN games g ON pg.game_id = g.id
        WHERE pg.user_id = ?
        ORDER BY pg.played_at DESC
    """
    return fetch_all(SQL, [user_id])

def mark_game_as_played(user_id, game_id, rating=None, notes=None):
    """Mark a game as played for a user"""
    SQL = """
        INSERT INTO played_games (user_id, game_id, rating, notes)
        VALUES (?, ?, ?, ?)
    """
    played_id = execute_query(SQL, [user_id, game_id, rating, notes])
    return get_played_game(played_id)

def get_played_game(played_id):
    """Get a single played game record"""
    SQL = """
        SELECT 
            pg.*,
            g.game_name
        FROM played_games pg
        JOIN games g ON pg.game_id = g.id
        WHERE pg.id = ?
    """
    return fetch_one(SQL, [played_id])

def check_if_played(user_id, game_id):
    """Check if user has played a specific game"""
    SQL = """
        SELECT COUNT(*) as count
        FROM played_games
        WHERE user_id = ? AND game_id = ?
    """
    result = fetch_one(SQL, [user_id, game_id])
    return result['count'] > 0 if result else False

def unmark_game_as_played(user_id, game_id):
    """Remove a game from user's played list"""
    SQL = """
        DELETE FROM played_games
        WHERE user_id = ? AND game_id = ?
    """
    execute_query(SQL, [user_id, game_id])
    return {"message": "Game removed from played list"}

def update_played_game(user_id, game_id, rating=None, notes=None):
    """Update rating or notes for a played game"""
    updates = []
    params = []
    
    if rating is not None:
        updates.append("rating = ?")
        params.append(rating)
    
    if notes is not None:
        updates.append("notes = ?")
        params.append(notes)
    
    if not updates:
        return None
    
    params.extend([user_id, game_id])
    
    SQL = f"""
        UPDATE played_games
        SET {', '.join(updates)}
        WHERE user_id = ? AND game_id = ?
    """
    execute_query(SQL, params)
    return {"message": "Played game updated"}

def get_games_batch_with_played_status(game_ids, user_id):
    """Get multiple games with their played status for a user - for Agent 1"""
    placeholders = ','.join(['?' for _ in game_ids])
    SQL = f"""
        SELECT 
            g.*,
            f.franchise_name,
            s.system_name,
            CASE WHEN pg.id IS NOT NULL THEN 1 ELSE 0 END as played
        FROM games g
        LEFT JOIN franchises f ON g.franchise_id = f.id
        LEFT JOIN systems s ON g.system_id = s.id
        LEFT JOIN played_games pg ON g.id = pg.game_id AND pg.user_id = ?
        WHERE g.id IN ({placeholders})
    """
    return fetch_all(SQL, [user_id] + game_ids)