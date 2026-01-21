"""FastAPI application entry point."""
from dotenv import load_dotenv
load_dotenv()  # Load .env before any other imports that might use env vars

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.database import init_db, seed_db
from app.routes import employees, review, inbox, manager

app = FastAPI(
    title="360 Feedback Tool",
    description="A lightweight prototype for 360-degree feedback collection with AI-powered summaries",
    version="1.0.0"
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(employees.router, prefix="/api", tags=["employees"])
app.include_router(review.router, prefix="/api", tags=["review"])
app.include_router(inbox.router, prefix="/api", tags=["inbox"])
app.include_router(manager.router, prefix="/api", tags=["manager"])

# Serve static files
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.on_event("startup")
def startup():
    """Initialize and seed database on startup."""
    init_db()
    seed_db()


@app.get("/")
def serve_index():
    """Serve landing page."""
    return FileResponse(static_dir / "index.html")


@app.get("/nominate")
def serve_nominate():
    """Serve employee nomination page."""
    return FileResponse(static_dir / "nominate.html")


@app.get("/review/{token}")
def serve_review(token: str):
    """Serve reviewer feedback form."""
    return FileResponse(static_dir / "review.html")


@app.get("/inbox/{email}")
def serve_inbox(email: str):
    """Serve reviewer inbox page."""
    return FileResponse(static_dir / "inbox.html")


@app.get("/manager/{employee_id}")
def serve_manager(employee_id: int):
    """Serve manager dashboard."""
    return FileResponse(static_dir / "manager.html")
