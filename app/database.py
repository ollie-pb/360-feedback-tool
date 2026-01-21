"""SQLite database connection, schema, and seed data."""
import sqlite3
import secrets
import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

# Use /tmp on Vercel (serverless), local file otherwise
if os.environ.get("VERCEL"):
    DATABASE_PATH = Path("/tmp/feedback.db")
else:
    DATABASE_PATH = Path(__file__).parent.parent / "feedback.db"


def get_db():
    """Dependency for FastAPI endpoints."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize database schema."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS reviewers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL REFERENCES employees(id),
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            relationship TEXT NOT NULL CHECK(relationship IN ('manager', 'peer', 'direct_report', 'xfn')),
            frequency TEXT NOT NULL CHECK(frequency IN ('weekly', 'monthly', 'rarely')),
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reviewer_id INTEGER NOT NULL REFERENCES reviewers(id),
            start_doing TEXT NOT NULL,
            stop_doing TEXT NOT NULL,
            continue_doing TEXT NOT NULL,
            example TEXT NOT NULL,
            additional TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL REFERENCES employees(id),
            content TEXT NOT NULL,
            weighting_explanation TEXT,
            finalised BOOLEAN DEFAULT FALSE,
            finalised_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_reviewers_employee_id ON reviewers(employee_id);
        CREATE INDEX IF NOT EXISTS idx_reviewers_token ON reviewers(token);
        CREATE INDEX IF NOT EXISTS idx_reviewers_email ON reviewers(email);
        CREATE INDEX IF NOT EXISTS idx_reviews_reviewer_id ON reviews(reviewer_id);
        CREATE INDEX IF NOT EXISTS idx_summaries_employee_id ON summaries(employee_id);
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Seed database with test data for demo."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    # Check if already seeded
    cursor = conn.execute("SELECT COUNT(*) as count FROM employees")
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return

    # Create employee: Alex Chen
    conn.execute(
        "INSERT INTO employees (name, email) VALUES (?, ?)",
        ("Alex Chen", "alex.chen@company.com")
    )
    employee_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Create reviewers with tokens
    reviewers_data = [
        ("Sam Taylor", "sam.taylor@company.com", "manager", "weekly", "sam-taylor-token-abc123"),
        ("Jordan Lee", "jordan.lee@company.com", "peer", "weekly", "jordan-lee-token-def456"),
        ("Casey Morgan", "casey.morgan@company.com", "direct_report", "monthly", "casey-morgan-token-ghi789"),
        ("Riley Kumar", "riley.kumar@company.com", "xfn", "rarely", "riley-kumar-token-jkl012"),
    ]

    reviewer_ids = []
    for name, email, relationship, frequency, token in reviewers_data:
        conn.execute(
            "INSERT INTO reviewers (employee_id, name, email, relationship, frequency, token) VALUES (?, ?, ?, ?, ?, ?)",
            (employee_id, name, email, relationship, frequency, token)
        )
        reviewer_ids.append(conn.execute("SELECT last_insert_rowid()").fetchone()[0])

    # Add submitted reviews for first 3 reviewers (Sam, Jordan, Casey)
    reviews_data = [
        (reviewer_ids[0], "Delegate more complex technical decisions to senior engineers",
         "Stop micromanaging code review comments on minor style issues",
         "Continue providing clear context on business requirements during sprint planning",
         "During last quarter's API redesign, Alex spent significant time reviewing every PR line-by-line. While thorough, this created bottlenecks.",
         "Alex has grown significantly in communication skills this year."),
        (reviewer_ids[1], "Start facilitating more cross-team knowledge sharing sessions",
         "Stop taking on too many parallel workstreams - focus improves quality",
         "Continue being the go-to person for debugging complex production issues",
         "When we had the database outage in October, Alex was instrumental in identifying the root cause within 30 minutes.",
         None),
        (reviewer_ids[2], "Start providing more regular 1:1 feedback rather than saving it for reviews",
         "Stop context-switching between projects mid-sprint",
         "Continue the mentorship approach - the pairing sessions have been invaluable",
         "Alex paired with me for two weeks on the authentication refactor. I learned more in those sessions than in months of solo work.",
         "Really appreciate the psychological safety Alex creates in our team."),
    ]

    for reviewer_id, start, stop, cont, example, additional in reviews_data:
        conn.execute(
            "INSERT INTO reviews (reviewer_id, start_doing, stop_doing, continue_doing, example, additional) VALUES (?, ?, ?, ?, ?, ?)",
            (reviewer_id, start, stop, cont, example, additional)
        )

    conn.commit()
    conn.close()
