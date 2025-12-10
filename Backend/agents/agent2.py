from dotenv import load_dotenv
load_dotenv()

import os
import json
import re
from groq import Groq
from agents.agent1 import get_user_context
from db.query import games as game_functions

# Configure Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def agent2_generate_recommendations(user_query: str, user_id: int, num_recommendations: int = 5):
    """
    Agent 2: Recommendation Engine (using Groq)
    Takes user query, gets context from Agent 1, generates game recommendations
    """
    
    # Step 1: Get user context from Agent 1
    user_context = get_user_context(user_id)
    played_game_names = [game['game_name'] for game in user_context['played_games']]
    played_genres = list(set([game['genre'] for game in user_context['played_games']]))
    
    # Step 2: Generate candidate games
    candidate_prompt = f"""
Generate 15 game titles that match this request:

User query: "{user_query}"
User has played: {', '.join(played_game_names)}
User enjoys: {', '.join(played_genres)}

Return ONLY a JSON array of titles:
["Game 1", "Game 2", ...]
"""
    
    candidate_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": candidate_prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    candidate_text = candidate_response.choices[0].message.content.strip()
    candidate_text = candidate_text.replace('```json', '').replace('```', '').strip()
    
    try:
        candidate_games = json.loads(candidate_text)
    except:
        print(f"Failed to parse candidates: {candidate_text}")
        candidate_games = []
    
    print(f"\n🤖 Agent 2 generated {len(candidate_games)} candidates:")
    print(candidate_games[:5], "...")
    
    # Step 3: Match with database
    all_games = game_functions.get_all_games()
    matching_games = []
    
    for candidate in candidate_games:
        for db_game in all_games:
            if candidate.lower() in db_game['game_name'].lower() or db_game['game_name'].lower() in candidate.lower():
                if db_game['game_name'] not in played_game_names:
                    matching_games.append(db_game)
                    break
    
    print(f"\n📊 Found {len(matching_games)} matching games in database")
    
    # Add more unplayed games if needed
    if len(matching_games) < num_recommendations:
        unplayed_games = [g for g in all_games if g['game_name'] not in played_game_names]
        for game in unplayed_games:
            if game not in matching_games:
                matching_games.append(game)
            if len(matching_games) >= 10:
                break
    
    # Step 4: Generate final recommendations
    game_list = json.dumps([{
        'title': g['game_name'],
        'genre': g['genre'],
        'description': g['description']
    } for g in matching_games[:10]], indent=2)
    
    final_prompt = f"""
Select {num_recommendations} games from this list for: "{user_query}"

User played: {', '.join(played_game_names[:5])}

Games:
{game_list}

Return ONLY valid JSON array. Keep explanations to ONE SHORT sentence each:
[
  {{"title": "Game Name", "why_recommended": "Brief reason"}}
]
"""
    
    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0.3,
        max_tokens=2000
    )
    
    final_text = final_response.choices[0].message.content.strip()
    final_text = final_text.replace('```json', '').replace('```', '').strip()
    
    print(f"\n🔍 Raw response:\n{final_text[:200]}...\n")
    
    json_match = re.search(r'\[.*\]', final_text, re.DOTALL)
    if json_match:
        final_text = json_match.group(0)
    
    try:
        recommendations = json.loads(final_text)
    except Exception as e:
        print(f"❌ Failed to parse: {e}")
        recommendations = []
    
    return {
        "query": user_query,
        "user_id": user_id,
        "recommendations": recommendations
    }

# Test function
if __name__ == "__main__":
    print("🎮 Testing Agent 2: Game Recommendation Engine\n")
    
    result = agent2_generate_recommendations(
        user_query="I want a challenging action RPG with great boss fights",
        user_id=1,
        num_recommendations=5
    )
    
    print("\n✨ FINAL RECOMMENDATIONS:\n")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"{i}. {rec['title']}")
        print(f"   Why: {rec['why_recommended']}\n")