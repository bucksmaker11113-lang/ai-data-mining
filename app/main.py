from fastapi import FastAPI
from app.routes.api_routes import router as api_routes

app = FastAPI()

@app.get("/")
def home():
    return {"status": "AI Data Mining Backend Running"}

app.include_router(api_routes, prefix="/api")
