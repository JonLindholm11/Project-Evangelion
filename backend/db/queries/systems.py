from db.client import fetch_all, fetch_one, execute_query

def create_system(system_name, system_img):
    SQL = """
        INSERT INTO systems
        (system_name, system_img)
        VALUES (?, ?)
    """
    system_id = execute_query(SQL, [system_name, system_img])
    return get_system(system_id)

def get_all_systems():
    SQL = """
        SELECT *
        FROM systems
    """
    return fetch_all(SQL)

def get_system(id):
    SQL = """
        SELECT *
        FROM systems
        WHERE id = ?
    """
    return fetch_one(SQL, [id])

def update_system(id, system_name, system_img):
    SQL = """
        UPDATE systems
        SET
            system_name = ?,
            system_img = ?
        WHERE id = ?
    """
    execute_query(SQL, [system_name, system_img, id])
    return get_system(id)

def delete_system(system_id):
    SQL = """
        DELETE FROM systems
        WHERE id = ?
    """
    execute_query(SQL, [system_id])
    return {"message": "System deleted"}