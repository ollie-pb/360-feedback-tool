"""Feedback cycle API routes."""
import secrets
from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional

from app.database import get_db, get_or_create_user
from app.models import CycleCreate, CycleResponse, ReviewerCreate, ReviewerResponse

router = APIRouter()


@router.post("/cycles", response_model=CycleResponse)
def create_cycle(
    cycle: CycleCreate,
    x_user_email: Optional[str] = Header(None),
    db=Depends(get_db)
):
    """Create a new feedback cycle for an employee."""
    cur = db.cursor()

    # Get or create the subject user (the person being reviewed)
    subject_user = get_or_create_user(cycle.email, cycle.name)
    subject_user_id = subject_user["id"]

    # Determine who created the cycle
    # If logged in, use that user; otherwise, assume self-nomination
    if x_user_email:
        cur.execute("SELECT id FROM users WHERE email = %s", (x_user_email,))
        creator = cur.fetchone()
        created_by_user_id = creator["id"] if creator else subject_user_id
    else:
        created_by_user_id = subject_user_id

    # Create the feedback cycle
    cur.execute(
        """INSERT INTO feedback_cycles (subject_user_id, created_by_user_id, title)
           VALUES (%s, %s, %s) RETURNING *""",
        (subject_user_id, created_by_user_id, cycle.title)
    )
    row = cur.fetchone()
    db.commit()

    return CycleResponse(
        id=row["id"],
        subject_user_id=row["subject_user_id"],
        created_by_user_id=row["created_by_user_id"],
        title=row["title"],
        status=row["status"],
        created_at=row["created_at"],
        subject_name=cycle.name
    )


@router.post("/cycles/{cycle_id}/reviewers", response_model=ReviewerResponse)
def add_reviewer(
    cycle_id: int,
    reviewer: ReviewerCreate,
    db=Depends(get_db)
):
    """Add a reviewer to a feedback cycle. Returns unique token."""
    cur = db.cursor()

    # Verify cycle exists
    cur.execute("SELECT id FROM feedback_cycles WHERE id = %s", (cycle_id,))
    cycle = cur.fetchone()

    if not cycle:
        raise HTTPException(status_code=404, detail="Feedback cycle not found")

    # Check for duplicate reviewer email for this cycle
    cur.execute(
        "SELECT id FROM reviewers WHERE cycle_id = %s AND email = %s",
        (cycle_id, reviewer.email)
    )
    existing = cur.fetchone()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="This reviewer has already been added for this cycle"
        )

    # Validate relationship and frequency
    valid_relationships = {"manager", "peer", "direct_report", "xfn"}
    valid_frequencies = {"weekly", "monthly", "rarely"}

    if reviewer.relationship not in valid_relationships:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid relationship. Must be one of: {valid_relationships}"
        )

    if reviewer.frequency not in valid_frequencies:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid frequency. Must be one of: {valid_frequencies}"
        )

    # Generate unique token
    token = secrets.token_urlsafe(32)

    cur.execute(
        """INSERT INTO reviewers (cycle_id, name, email, relationship, frequency, token)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
        (cycle_id, reviewer.name, reviewer.email, reviewer.relationship, reviewer.frequency, token)
    )
    row = cur.fetchone()
    db.commit()

    return ReviewerResponse(
        id=row["id"],
        cycle_id=row["cycle_id"],
        name=row["name"],
        email=row["email"],
        relationship=row["relationship"],
        frequency=row["frequency"],
        token=row["token"],
        created_at=row["created_at"],
        has_submitted=False
    )


# Legacy endpoint for backward compatibility
@router.post("/employees")
def create_employee_legacy(cycle: CycleCreate, x_user_email: Optional[str] = Header(None), db=Depends(get_db)):
    """Legacy endpoint - redirects to create_cycle."""
    return create_cycle(cycle, x_user_email, db)


@router.post("/employees/{employee_id}/reviewers")
def add_reviewer_legacy(employee_id: int, reviewer: ReviewerCreate, db=Depends(get_db)):
    """Legacy endpoint - redirects to add_reviewer."""
    return add_reviewer(employee_id, reviewer, db)
