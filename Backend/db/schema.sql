DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS systems;
DROP TABLE IF EXISTS franchises;
DROP TABLE IF EXISTS games;

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_verified BOOLEAN DEFAULT 0
);

CREATE TABLE systems(
    id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_img TEXT
);

CREATE TABLE franchises(
    id INTEGER PRIMARY KEY,
    system_id INTEGER REFERENCES systems(id) NOT NULL,
    franchise_name TEXT NOT NULL,
    franchise_img TEXT
);

CREATE TABLE games(
    id INTEGER PRIMARY KEY,
    franchise_id INTEGER REFERENCES franchises(id) NOT NULL,
    system_id INTEGER REFERENCES systems(id) NOT NULL,
    game_name TEXT NOT NULL,
    game_img TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);