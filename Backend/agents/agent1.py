import os
from groq import Groq
from dotenv import load_dotenv
from db.query import games as game_functions
from db.query import playedGames as played_games_functions

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def query_games_with_played_status(game_ids: list, user_id: int):
    """
    Agent 1's main function: Given a list of game IDs and a user,
    return game data with played status
    """
    result = played_games_functions.get_games_batch_with_played_status(game_ids, user_id)
    return result

def get_user_context(user_id: int):
    """
    Get user's played games for context
    """
    played_games = played_games_functions.get_user_played_games(user_id)
    return {
        "played_games": played_games,
        "played_count": len(played_games)
    }

def agent1_process_request(prompt: str, user_id: int):
    """
    Agent 1: Database Oracle
    Receives requests from Agent 2 and returns relevant game data
    """
    
    # Get user context
    user_context = get_user_context(user_id)
    
    # Build context for Agent 1
    context = f"""
You are Agent 1, the Database Oracle for a game recommendation system.
You have access to a games database with 30 games across various genres and platforms.

User {user_id} has played {user_context['played_count']} games:
{[game['game_name'] for game in user_context['played_games']]}

Your job: When Agent 2 asks you about games or user history, provide accurate database information.

Current request from Agent 2: {prompt}

Respond with relevant information from the database.
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Agent 1, a database oracle that provides game information."},
            {"role": "user", "content": context}
        ],
        temperature=0.1,  # Keep it factual
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# Test function
if __name__ == "__main__":
    # Test Agent 1
    test_response = agent1_process_request(
        "What strategy games has this user played?",
        user_id=1
    )
    print("Agent 1 Response:")
    print(test_response)