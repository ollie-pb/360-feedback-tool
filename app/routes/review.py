"""Review submission API routes."""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.database import get_db
from app.models import ReviewContext, ReviewSubmit, ReviewResponse
from app.services.summarisation import regenerate_summary_for_cycle

router = APIRouter()


@router.get("/review/{token}", response_model=ReviewContext)
def get_review_context(token: str, db=Depends(get_db)):
    """Get context for a review form (employee name, relationship)."""
    cur = db.cursor()

    cur.execute(
        """SELECT r.name as reviewer_name, r.relationship, r.id as reviewer_id,
                  u.name as employee_name
           FROM reviewers r
           JOIN feedback_cycles fc ON r.cycle_id = fc.id
           JOIN users u ON fc.subject_user_id = u.id
           WHERE r.token = %s""",
        (token,)
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Invalid review link")

    # Check if already submitted
    cur.execute(
        "SELECT id FROM reviews WHERE reviewer_id = %s",
        (row["reviewer_id"],)
    )
    submitted = cur.fetchone()

    return ReviewContext(
        employee_name=row["employee_name"],
        relationship=row["relationship"],
        reviewer_name=row["reviewer_name"],
        already_submitted=submitted is not None
    )


@router.post("/review/{token}", response_model=ReviewResponse)
def submit_review(
    token: str,
    review: ReviewSubmit,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    """Submit feedback for a review."""
    cur = db.cursor()

    # Get reviewer info including cycle_id for background task
    cur.execute(
        "SELECT id, cycle_id FROM reviewers WHERE token = %s",
        (token,)
    )
    reviewer = cur.fetchone()

    if not reviewer:
        raise HTTPException(status_code=404, detail="Invalid review link")

    # Check if already submitted
    cur.execute(
        "SELECT id FROM reviews WHERE reviewer_id = %s",
        (reviewer["id"],)
    )
    existing = cur.fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted")

    # Insert review
    cur.execute(
        """INSERT INTO reviews (reviewer_id, start_doing, stop_doing, continue_doing, example, additional)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
        (reviewer["id"], review.start_doing, review.stop_doing, review.continue_doing, review.example, review.additional)
    )
    row = cur.fetchone()
    db.commit()

    # Trigger summary regeneration in background
    background_tasks.add_task(regenerate_summary_for_cycle, reviewer["cycle_id"])

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
