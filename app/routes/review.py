"""Review submission API routes."""
import sqlite3
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import ReviewContext, ReviewSubmit, ReviewResponse

router = APIRouter()


@router.get("/review/{token}", response_model=ReviewContext)
def get_review_context(token: str, db: sqlite3.Connection = Depends(get_db)):
    """Get context for a review form (employee name, relationship)."""
    row = db.execute(
        """SELECT r.name as reviewer_name, r.relationship, e.name as employee_name, r.id as reviewer_id
           FROM reviewers r
           JOIN employees e ON r.employee_id = e.id
           WHERE r.token = ?""",
        (token,)
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Invalid review link")

    # Check if already submitted
    submitted = db.execute(
        "SELECT id FROM reviews WHERE reviewer_id = ?",
        (row["reviewer_id"],)
    ).fetchone()

    return ReviewContext(
        employee_name=row["employee_name"],
        relationship=row["relationship"],
        reviewer_name=row["reviewer_name"],
        already_submitted=submitted is not None
    )


@router.post("/review/{token}", response_model=ReviewResponse)
def submit_review(token: str, review: ReviewSubmit, db: sqlite3.Connection = Depends(get_db)):
    """Submit feedback for a review."""
    # Get reviewer info
    reviewer = db.execute(
        "SELECT id FROM reviewers WHERE token = ?",
        (token,)
    ).fetchone()

    if not reviewer:
        raise HTTPException(status_code=404, detail="Invalid review link")

    # Check if already submitted
    existing = db.execute(
        "SELECT id FROM reviews WHERE reviewer_id = ?",
        (reviewer["id"],)
    ).fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted")

    # Insert review
    cursor = db.execute(
        """INSERT INTO reviews (reviewer_id, start_doing, stop_doing, continue_doing, example, additional)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (reviewer["id"], review.start_doing, review.stop_doing, review.continue_doing, review.example, review.additional)
    )
    db.commit()

    review_id = cursor.lastrowid
    row = db.execute(
        "SELECT * FROM reviews WHERE id = ?",
        (review_id,)
    ).fetchone()

    return ReviewResponse(
        id=row["id"],
        reviewer_id=row["reviewer_id"],
        start_doing=row["start_doing"],
        stop_doing=row["stop_doing"],
        continue_doing=row["continue_doing"],
        example=row["example"],
        additional=row["additional"],
        submitted_at=row["submitted_at"]
    )
