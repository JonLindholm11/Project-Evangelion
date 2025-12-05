from db.client import fetch_all, fetch_one, execute_query

def create_game(franchise_id, system_id, game_name, game_img=None, description=None):
    SQL = """
        INSERT INTO games
        (franchise_id, system_id, game_name, game_img, description)
        VALUES (?, ?, ?, ?, ?)
    """
    game_id = execute_query(SQL, [franchise_id, system_id, game_name, game_img, description])
    return get_game(game_id)

def get_all_games():
    SQL = """
        SELECT
            g.*,
            f.franchise_name,
            s.system_name
        FROM games g
        LEFT JOIN franchises f ON g.franchise_id = f.id
        LEFT JOIN systems s ON g.system_id = s.id
    """
    return fetch_all(SQL)
    
def get_game(id):
    SQL = """
        SELECT
            g.*,
            f.franchise_name,
            s.system_name
        FROM games g
        LEFT JOIN franchises f ON g.franchise_id = f.id
        LEFT JOIN systems s ON g.system_id = s.id
        WHERE g.id = ?
    """
    return fetch_one(SQL, [id])

def get_games_by_franchise(franchise_id):
    SQL = """
        SELECT
            g.*,
            f.franchise_name,
            s.system_name
        FROM games g
        LEFT JOIN franchises f ON g.franchise_id = f.id
        LEFT JOIN systems s ON g.system_id = s.id
        WHERE g.franchise_id = ?
    """
    return fetch_all(SQL, [franchise_id])

def update_game(id, franchise_id, system_id, game_name, game_img, description):
    SQL = """
    UPDATE games
    SET 
        franchise_id = ?,
        system_id = ?,
        game_name = ?,
        game_img = ?,
        description = ?
    WHERE id = ?
    """
    execute_query(SQL, [franchise_id, system_id, game_name, game_img, description, id])
    return get_game(id)

def delete_game(game_id):
    SQL = """
        DELETE FROM games
        WHERE id = ?
    """
    execute_query(SQL, [game_id])
    return {"message": "Game deleted"}