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
    franchise_name TEXT NOT NULL,
    franchise_img TEXT
);

CREATE TABLE games(
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
);

CREATE TABLE played_games(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    game_id INTEGER REFERENCES games(id) NOT NULL,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    notes TEXT,
    UNIQUE(user_id, game_id)
);