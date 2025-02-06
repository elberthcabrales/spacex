from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Use FastAPI's CORSMiddleware
from app.api.routers import rockets, health, launches, starlinks, dashboard
from app.infrastructure.db.database import init_db

app = FastAPI(title="SpaceX API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def startup():
    """Initialize database on startup."""
    init_db()

# Register routers
app.include_router(health.router, prefix="/api")
app.include_router(rockets.router, prefix="/api")
app.include_router(launches.router, prefix="/api")
app.include_router(starlinks.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")