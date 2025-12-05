import json
from db.client import execute_query
import user_functions
import system_functions
import franchise_functions
import game_functions

def seed_users():
    """Seed users from JSON file"""
    try:
        with open('seed_data/users.json', 'r') as f:
            data = json.load(f)
            
        for user in data['users']:
            user_functions.create_user(
                user['email'],
                user['password'],
                user['is_verified']
            )
        print("Users seeded")
    except FileNotFoundError:
        print("users.json not found, skipping...")
    except Exception as e:
        print(f"Error seeding users: {e}")
        raise

def seed_systems():
    """Seed systems from JSON file"""
    try:
        with open('seed_data/systems.json', 'r') as f:
            data = json.load(f)
            
        for system in data['systems']:
            system_functions.create_system(
                system['system_name'],
                system['system_img']
            )
        print("Systems seeded")
    except FileNotFoundError:
        print("systems.json not found, skipping...")
    except Exception as e:
        print(f"Error seeding systems: {e}")
        raise

def seed_franchises():
    """Seed franchises from JSON file"""
    try:
        with open('seed_data/franchises.json', 'r') as f:
            data = json.load(f)
            
        for franchise in data['franchises']:
            franchise_functions.create_franchise(
                franchise['system_id'],
                franchise['franchise_name'],
                franchise['franchise_img']
            )
        print("Franchises seeded")
    except FileNotFoundError:
        print("franchises.json not found, skipping...")
    except Exception as e:
        print(f"Error seeding franchises: {e}")
        raise

def seed_games():
    """Seed games from JSON file"""
    try:
        with open('seed_data/games.json', 'r') as f:
            data = json.load(f)
            
        for game in data['games']:
            game_functions.create_game(
                game['franchise_id'],
                game['system_id'],
                game['game_name'],
                game.get('game_img'),
                game.get('description')  
            )
        print("Games seeded")
    except FileNotFoundError:
        print("games.json not found, skipping...")
    except Exception as e:
        print(f"Error seeding games: {e}")
        raise

def seed_database():
    """Main function to seed the entire database"""
    try:
        print("Starting database seeding...")
        print("=" * 50)
        
        seed_users()
        seed_systems()
        seed_franchises()
        seed_games()
        
        print("=" * 50)
        print("Database seeding completed successfully!")
        
    except Exception as error:
        print("=" * 50)
        print(f"Error seeding database: {error}")
        raise

if __name__ == "__main__":
    seed_database()