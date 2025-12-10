# seed_database.py
import sqlite3
import json
from pathlib import Path

def seed_database():
    # Connect to database
    conn = sqlite3.connect('games.db')
    cur = conn.cursor()
    
    # Create tables
    print("Creating tables...")
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS systems(
            id INTEGER PRIMARY KEY,
            system_name TEXT NOT NULL,
            system_img TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS franchises(
            id INTEGER PRIMARY KEY,
            franchise_name TEXT NOT NULL,
            franchise_img TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY,
            franchise_id INTEGER REFERENCES franchises(id),
            system_id INTEGER REFERENCES systems(id) NOT NULL,
            publisher TEXT NOT NULL,
            game_name TEXT NOT NULL,
            game_img TEXT,
            genre TEXT,
            release_year INTEGER,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS played_games(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id) NOT NULL,
            game_id INTEGER REFERENCES games(id) NOT NULL,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            notes TEXT,
            UNIQUE(user_id, game_id)
        )
    """)
    
    # Load and insert systems
    print("Seeding systems...")
    with open('seed/systems.json', 'r') as f:
        systems = json.load(f)
        for system in systems:
            cur.execute("""
                INSERT OR IGNORE INTO systems (id, system_name, system_img)
                VALUES (?, ?, ?)
            """, (system['id'], system['system_name'], system['system_img']))
    
    # Load and insert franchises
    print("Seeding franchises...")
    with open('seed/franchises.json', 'r') as f:
        franchises = json.load(f)
        for franchise in franchises:
            cur.execute("""
                INSERT OR IGNORE INTO franchises (id, franchise_name, franchise_img)
                VALUES (?, ?, ?)
            """, (franchise['id'], franchise['franchise_name'], franchise['franchise_img']))
    
    # Load and insert games
    print("Seeding games...")
    with open('seed/games.json', 'r') as f:
        games = json.load(f)
        for game in games:
            cur.execute("""
                INSERT OR IGNORE INTO games 
                (id, franchise_id, system_id, publisher, game_name, game_img, genre, release_year, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                game['id'], game['franchise_id'], game['system_id'], 
                game['publisher'], game['game_name'], game['game_img'],
                game['genre'], game['release_year'], game['description']
            ))
    
    # Create test user
    print("Creating test user...")
    cur.execute("""
        INSERT OR IGNORE INTO users (id, username, email, password_hash)
        VALUES (1, 'test_user', 'test@example.com', 'hashed_password_here')
    """)
    
    # Load and insert played games
    print("Seeding played games...")
    with open('seed/played_games.json', 'r') as f:
        played_games = json.load(f)
        for played in played_games:
            cur.execute("""
                INSERT OR IGNORE INTO played_games (user_id, game_id, rating, notes)
                VALUES (?, ?, ?, ?)
            """, (played['user_id'], played['game_id'], played.get('rating'), played.get('notes')))
    
    conn.commit()
    print("✅ Database seeded successfully!")
    
    # Verify counts
    cur.execute("SELECT COUNT(*) FROM systems")
    print(f"Systems: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM franchises")
    print(f"Franchises: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM games")
    print(f"Games: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM played_games")
    print(f"Played games: {cur.fetchone()[0]}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    seed_database()
