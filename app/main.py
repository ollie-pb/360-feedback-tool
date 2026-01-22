"""FastAPI application entry point."""
from dotenv import load_dotenv
load_dotenv()  # Load .env before any other imports that might use env vars

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.database import init_db, seed_demo_data
from app.routes import cycles, review, inbox, manager, auth

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
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(cycles.router, prefix="/api", tags=["cycles"])
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
    seed_demo_data()


@app.get("/")
def serve_index():
    """Serve landing page."""
    return FileResponse(static_dir / "index.html")


@app.get("/dashboard")
def serve_dashboard():
    """Serve user dashboard page."""
    return FileResponse(static_dir / "dashboard.html")


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


@app.get("/cycle/{cycle_id}")
def serve_cycle(cycle_id: str):
    """Serve cycle management page."""
    return FileResponse(static_dir / "manager.html")


# Legacy route for backward compatibility
@app.get("/manager/{employee_identifier}")
def serve_manager(employee_identifier: str):
    """Serve manager dashboard (legacy URL)."""
    return FileResponse(static_dir / "manager.html")
