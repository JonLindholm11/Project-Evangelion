from fastapi import APIRouter

router = APIRouter(tags=["health"])

# GET /ping - Keep-alive endpoint for UptimeRobot
@router.get("/ping")
async def ping():
    """
    Keep-alive endpoint to prevent Render from spinning down.
    Used by UptimeRobot to ping the server every 5 minutes.
    """
    return {"status": "alive"}