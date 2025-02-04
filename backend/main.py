from fastapi import FastAPI
from app.api.routers import rockets, health, launches, starlinks
from app.infrastructure.db.database import init_db

app = FastAPI(title="SpaceX API")

@app.on_event("startup")
def startup():
    """Initialize database on startup."""
    init_db()

# Register routers
app.include_router(health.router, prefix="/api")
app.include_router(rockets.router, prefix="/api")
app.include_router(launches.router, prefix="/api")
app.include_router(starlinks.router, prefix="/api")
