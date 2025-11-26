from db.client import get_connection


def create_game(franchise_id, system_id, game_name, game_file, game_img=None, description=None):
    SQL = """
        INSERT INTO games
        (franchise_id, system_id, game_name, game_file, game_img, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL, [franchise_id, system_id, game_name, game_file, game_img, description])
    conn.commit()
    
    game_id = cursor.lastrowid
    cursor.execute("SELECT * FROM games WHERE id = ?", [game_id])
    game = cursor.fetchone()
    conn.close()
    
    return dict(game)

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
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL)
    games = cursor.fetchall()
    conn.close() 
    
    return [dict(game) for game in games]
    
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
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL, [id])
    game = cursor.fetchone() 
    conn.close() 
    
    return dict(game) if game else None

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

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL, [franchise_id])
    games = cursor.fetchall() 
    conn.close() 
    
    return [dict(game) for game in games]

def update_game(id, franchise_id, system_id, game_name, game_file, game_img, description):
    SQL = """
    UPDATE games
    SET 
        franchise_id = ?,
        system_id = ?,
        game_name = ?,
        game_file = ?,
        game_img = ?,
        description = ?
    WHERE id = ?
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL, [franchise_id, system_id, game_name, game_file, game_img, description, id])
    conn.commit()
    
    cursor.execute("SELECT * FROM games WHERE id = ?", [id])
    game = cursor.fetchone()
    conn.close()
    
    return dict(game) if game else None

def delete_game(game_id):
    SQL = """
        DELETE FROM games
        WHERE id = ?
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL, [game_id])
    conn.commit()
    conn.close()
    
    return {"message": "Game deleted"}