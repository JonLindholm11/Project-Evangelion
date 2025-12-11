from fastapi import FastAPI
from api import users as user_routes
from api import systems as system_routes
from api import games as game_routes
from api import franchises as franchise_routes
from api import ping as ping_routes
from api import playedGames as played_games_routes
from api import ai as aiRoutes

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(system_routes.router)
app.include_router(game_routes.router)
app.include_router(franchise_routes.router)
app.include_router(ping_routes.router)
app.include_router(played_games_routes.router)
app.include_router(aiRoutes.router)