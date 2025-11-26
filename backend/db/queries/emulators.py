from db.client import fetch_all, fetch_one, execute_query

def create_emulator(system_id, emulator_name, emulator_file, emulator_img):
    SQL = """
        INSERT INTO emulators
        (system_id, emulator_name, emulator_file, emulator_img)
        VALUES (?, ?, ?, ?)
    """
    emulator_id = execute_query(SQL, [system_id, emulator_name, emulator_file, emulator_img])
    return get_emulator(emulator_id)

def get_all_emulators():
    SQL = """
        SELECT
            e.*,
            s.system_name
        FROM emulators e
        LEFT JOIN systems s ON e.system_id = s.id
    """
    return fetch_all(SQL)
    
def get_emulator(id):
    SQL = """
        SELECT
            e.*,
            s.system_name
        FROM emulators e
        LEFT JOIN systems s ON e.system_id = s.id
        WHERE e.id = ?
    """
    return fetch_one(SQL, [id])

def update_emulator(id, system_id, emulator_name, emulator_file, emulator_img):
    SQL = """
    UPDATE emulators
    SET 
        system_id = ?,
        emulator_name = ?, 
        emulator_file = ?, 
        emulator_img = ?
    WHERE id = ?
    """
    execute_query(SQL, [system_id, emulator_name, emulator_file, emulator_img, id])
    return get_emulator(id)

def delete_emulator(emulator_id):
    SQL = """
        DELETE FROM emulators
        WHERE id = ?
    """
    execute_query(SQL, [emulator_id])
    return {"message": "Emulator deleted"}