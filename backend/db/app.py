from fastapi import FastAPI
import user_routes
import ping_routes

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(ping_routes.router)