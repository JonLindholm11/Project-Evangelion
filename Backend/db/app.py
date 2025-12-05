from fastapi import FastAPI
import user_routes
import system_routes
import game_routes
import franchise_routes
import ping_routes

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(system_routes.router)
app.include_router(game_routes.router)
app.include_router(franchise_routes.router)
app.include_router(ping_routes.router)