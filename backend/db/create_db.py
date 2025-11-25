import sqlite3

# Read your schema file
with open('schema.sql', 'r') as f:
    schema = f.read()

# Create database and execute schema
conn = sqlite3.connect('game_storage.db')
cursor = conn.cursor()
cursor.executescript(schema)
conn.commit()
conn.close()

print("Database created successfully!")