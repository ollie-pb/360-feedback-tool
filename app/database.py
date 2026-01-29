"""PostgreSQL database connection, schema, and seed data."""
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    """Get a database connection."""
    return psycopg2.connect(
        os.environ.get("POSTGRES_URL"),
        cursor_factory=RealDictCursor
    )


def get_db():
    """Dependency for FastAPI endpoints."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize database schema."""
    conn = get_connection()
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            is_demo BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS feedback_cycles (
            id SERIAL PRIMARY KEY,
            subject_user_id INTEGER NOT NULL REFERENCES users(id),
            created_by_user_id INTEGER NOT NULL REFERENCES users(id),
            manager_user_id INTEGER REFERENCES users(id),
            title TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS reviewers (
            id SERIAL PRIMARY KEY,
            cycle_id INTEGER NOT NULL REFERENCES feedback_cycles(id),
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            relationship TEXT NOT NULL,
            frequency TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id SERIAL PRIMARY KEY,
            reviewer_id INTEGER NOT NULL REFERENCES reviewers(id),
            start_doing TEXT NOT NULL,
            stop_doing TEXT NOT NULL,
            continue_doing TEXT NOT NULL,
            example TEXT NOT NULL,
            additional TEXT,
            submitted_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS summaries (
            id SERIAL PRIMARY KEY,
            cycle_id INTEGER NOT NULL REFERENCES feedback_cycles(id),
            content TEXT NOT NULL,
            weighting_explanation TEXT,
            finalised BOOLEAN DEFAULT FALSE,
            finalised_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_feedback_cycles_subject ON feedback_cycles(subject_user_id);
        CREATE INDEX IF NOT EXISTS idx_feedback_cycles_creator ON feedback_cycles(created_by_user_id);
        CREATE INDEX IF NOT EXISTS idx_feedback_cycles_manager ON feedback_cycles(manager_user_id);
        CREATE INDEX IF NOT EXISTS idx_reviewers_cycle ON reviewers(cycle_id);
        CREATE INDEX IF NOT EXISTS idx_reviewers_token ON reviewers(token);
        CREATE INDEX IF NOT EXISTS idx_reviewers_email ON reviewers(email);
        CREATE INDEX IF NOT EXISTS idx_reviews_reviewer ON reviews(reviewer_id);
        CREATE INDEX IF NOT EXISTS idx_summaries_cycle ON summaries(cycle_id);
    """)

    # Migration: Fix manager_user_id on demo cycles where Sam is reviewer with 'manager' relationship
    # but manager_user_id is not set on the cycle
    cur.execute("""
        UPDATE feedback_cycles fc
        SET manager_user_id = (SELECT id FROM users WHERE email = 'sam@demo.360feedback')
        WHERE fc.subject_user_id IN (SELECT id FROM users WHERE email = 'alex@demo.360feedback')
        AND fc.manager_user_id IS NULL
    """)

    conn.commit()
    cur.close()
    conn.close()


def seed_demo_data():
    """Seed database with demo users and sample feedback cycle."""
    conn = get_connection()
    cur = conn.cursor()

    # Check if demo users already exist
    cur.execute("SELECT COUNT(*) as count FROM users WHERE is_demo = TRUE")
    if cur.fetchone()["count"] > 0:
        cur.close()
        conn.close()
        return

    # Create demo users
    demo_users = [
        ("alex@demo.360feedback", "Alex Chen"),
        ("sam@demo.360feedback", "Sam Taylor"),
        ("jordan@demo.360feedback", "Jordan Lee"),
        ("casey@demo.360feedback", "Casey Morgan"),
        ("riley@demo.360feedback", "Riley Kumar"),
    ]

    user_ids = {}
    for email, name in demo_users:
        cur.execute(
            "INSERT INTO users (email, name, is_demo) VALUES (%s, %s, TRUE) RETURNING id",
            (email, name)
        )
        user_ids[email] = cur.fetchone()["id"]

    # Create a demo feedback cycle for Alex Chen (with Sam Taylor as manager)
    alex_id = user_ids["alex@demo.360feedback"]
    sam_id = user_ids["sam@demo.360feedback"]
    cur.execute(
        "INSERT INTO feedback_cycles (subject_user_id, created_by_user_id, manager_user_id, title) VALUES (%s, %s, %s, %s) RETURNING id",
        (alex_id, alex_id, sam_id, "Q4 2024 Review")
    )
    cycle_id = cur.fetchone()["id"]

    # Create reviewers with tokens
    reviewers_data = [
        ("Sam Taylor", "sam@demo.360feedback", "manager", "weekly", "demo-sam-token-abc123"),
        ("Jordan Lee", "jordan@demo.360feedback", "peer", "weekly", "demo-jordan-token-def456"),
        ("Casey Morgan", "casey@demo.360feedback", "direct_report", "monthly", "demo-casey-token-ghi789"),
        ("Riley Kumar", "riley@demo.360feedback", "xfn", "rarely", "demo-riley-token-jkl012"),
    ]

    reviewer_ids = []
    for name, email, relationship, frequency, token in reviewers_data:
        cur.execute(
            "INSERT INTO reviewers (cycle_id, name, email, relationship, frequency, token) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (cycle_id, name, email, relationship, frequency, token)
        )
        reviewer_ids.append(cur.fetchone()["id"])

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
        cur.execute(
            "INSERT INTO reviews (reviewer_id, start_doing, stop_doing, continue_doing, example, additional) VALUES (%s, %s, %s, %s, %s, %s)",
            (reviewer_id, start, stop, cont, example, additional)
        )

    conn.commit()
    cur.close()
    conn.close()


def get_or_create_user(email: str, name: str) -> dict:
    """Get existing user or create new one."""
    conn = get_connection()
    cur = conn.cursor()

    # Try to find existing user
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user:
        cur.close()
        conn.close()
        return dict(user)

    # Create new user
    cur.execute(
        "INSERT INTO users (email, name) VALUES (%s, %s) RETURNING *",
        (email, name)
    )
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(user)
