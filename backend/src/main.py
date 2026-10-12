from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.routes import router as api_router
from backend.src.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database schema on startup
    init_db()
    yield


# Initialize FastAPI application
app = FastAPI(
    title="AURA — Autonomous Multi-Agent Research Assistant",
    description="Backend API orchestrating LangGraph multi-agent research workflows.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # In production, specify frontend domain (e.g. http://localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],            # Allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    """Root redirect message."""
    return {"message": "Welcome to AURA API. Visit /docs for interactive Swagger documentation."}
