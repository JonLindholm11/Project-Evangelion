from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from typing import List, Optional
import jwt
import os
from datetime import datetime

from agents.agent2 import agent2_generate_recommendations

router = APIRouter(prefix="/api/ai", tags=["AI"])

# Models
class QueryRequest(BaseModel):
    query: str
    num_recommendations: Optional[int] = 5

class GameRecommendation(BaseModel):
    title: str
    why_recommended: str

class QueryResponse(BaseModel):
    query: str
    user_id: int
    recommendations: List[GameRecommendation]
    timestamp: str

# Auth
async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# Endpoints
@router.post("/query", response_model=QueryResponse)
async def post_query(request: QueryRequest, current_user: dict = Depends(verify_token)):
    user_id = current_user.get("user_id") or current_user.get("id")
    
    result = agent2_generate_recommendations(
        user_query=request.query,
        user_id=user_id,
        num_recommendations=request.num_recommendations
    )
    
    recommendations = [
        GameRecommendation(title=rec["title"], why_recommended=rec["why_recommended"])
        for rec in result["recommendations"]
    ]
    
    return QueryResponse(
        query=result["query"],
        user_id=result["user_id"],
        recommendations=recommendations,
        timestamp=datetime.now().isoformat()
    )

@router.get("/response")
async def get_response(current_user: dict = Depends(verify_token)):
    return {"status": "ok", "timestamp": datetime.now().isoformat()}