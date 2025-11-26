from db.client import fetch_all, fetch_one, execute_query

def create_franchise(system_id, franchise_name, franchise_img):
    SQL = """
        INSERT INTO franchises
        (system_id, franchise_name, franchise_img)
        VALUES (?, ?, ?)
    """
    franchise_id = execute_query(SQL, [system_id, franchise_name, franchise_img])
    return get_franchise(franchise_id)

def get_all_franchises():
    SQL = """
        SELECT
            f.*,
            s.system_name
        FROM franchises f
        LEFT JOIN systems s ON f.system_id = s.id
    """
    return fetch_all(SQL)

def get_franchise(id):
    SQL = """
        SELECT
            f.*,
            s.system_name
        FROM franchises f
        LEFT JOIN systems s ON f.system_id = s.id
        WHERE f.id = ?
    """
    return fetch_one(SQL, [id])

def update_franchise(id, system_id, franchise_name, franchise_img):
    SQL = """
        UPDATE franchises
        SET
            system_id = ?,
            franchise_name = ?,
            franchise_img = ?
        WHERE id = ?
    """
    execute_query(SQL, [system_id, franchise_name, franchise_img, id])
    return get_franchise(id)

def delete_franchise(franchise_id):
    SQL = """
        DELETE FROM franchises
        WHERE id = ?
    """
    execute_query(SQL, [franchise_id])
    return {"message": "franchise deleted"}