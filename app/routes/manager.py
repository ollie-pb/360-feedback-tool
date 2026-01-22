"""Manager dashboard API routes."""
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from app.database import get_db
from app.models import (
    CycleResponse, ReviewerWithStatus, SummaryResponse,
    SummaryUpdate, CycleDashboard, EmployeeResponse, ManagerDashboard
)
from app.services.summarisation import generate_summary

router = APIRouter()


@router.get("/manager/{cycle_identifier}", response_model=ManagerDashboard)
def get_manager_dashboard(cycle_identifier: str, db=Depends(get_db)):
    """Get manager dashboard with reviewers, statuses, and summary.

    Supports lookup by:
    - Cycle ID (integer)
    - Subject user name (string)
    """
    cur = db.cursor()

    # Try as integer ID first
    try:
        cycle_id = int(cycle_identifier)
        cur.execute(
            """SELECT fc.*, u.name as subject_name, u.email as subject_email
               FROM feedback_cycles fc
               JOIN users u ON fc.subject_user_id = u.id
               WHERE fc.id = %s""",
            (cycle_id,)
        )
        cycle = cur.fetchone()
    except ValueError:
        # Not an integer, try name lookup (finds most recent cycle for that person)
        cur.execute(
            """SELECT fc.*, u.name as subject_name, u.email as subject_email
               FROM feedback_cycles fc
               JOIN users u ON fc.subject_user_id = u.id
               WHERE u.name = %s
               ORDER BY fc.created_at DESC
               LIMIT 1""",
            (cycle_identifier,)
        )
        cycle = cur.fetchone()

    if not cycle:
        raise HTTPException(status_code=404, detail="Feedback cycle not found")

    cycle_id = cycle["id"]

    # Get reviewers with status
    cur.execute(
        """SELECT r.id, r.name, r.email, r.relationship, r.frequency,
                  (SELECT COUNT(*) FROM reviews WHERE reviewer_id = r.id) as has_review
           FROM reviewers r
           WHERE r.cycle_id = %s
           ORDER BY r.created_at""",
        (cycle_id,)
    )
    reviewers = cur.fetchall()

    reviewers_list = [
        ReviewerWithStatus(
            id=r["id"],
            name=r["name"],
            email=r["email"],
            relationship=r["relationship"],
            frequency=r["frequency"],
            status="submitted" if r["has_review"] > 0 else "pending"
        )
        for r in reviewers
    ]

    submitted_count = sum(1 for r in reviewers_list if r.status == "submitted")

    # Get summary if exists
    cur.execute("SELECT * FROM summaries WHERE cycle_id = %s", (cycle_id,))
    summary = cur.fetchone()

    summary_response = None
    if summary:
        summary_response = SummaryResponse(
            id=summary["id"],
            cycle_id=summary["cycle_id"],
            content=summary["content"],
            weighting_explanation=summary["weighting_explanation"],
            finalised=bool(summary["finalised"]),
            finalised_at=summary["finalised_at"],
            updated_at=summary["updated_at"]
        )

    # Return legacy format for compatibility
    return ManagerDashboard(
        employee=EmployeeResponse(
            id=cycle["id"],  # Use cycle ID as employee ID for compatibility
            name=cycle["subject_name"],
            email=cycle["subject_email"],
            created_at=cycle["created_at"]
        ),
        reviewers=reviewers_list,
        summary=summary_response,
        submitted_count=submitted_count,
        total_reviewers=len(reviewers_list)
    )


@router.put("/manager/{cycle_id}/summary", response_model=SummaryResponse)
def update_summary(cycle_id: int, update: SummaryUpdate, db=Depends(get_db)):
    """Edit summary content."""
    cur = db.cursor()

    # Check if summary exists
    cur.execute("SELECT * FROM summaries WHERE cycle_id = %s", (cycle_id,))
    summary = cur.fetchone()

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    if summary["finalised"]:
        raise HTTPException(status_code=400, detail="Summary is finalised and cannot be edited")

    # Update summary
    cur.execute(
        "UPDATE summaries SET content = %s, updated_at = %s WHERE cycle_id = %s",
        (update.content, datetime.now(), cycle_id)
    )
    db.commit()

    cur.execute("SELECT * FROM summaries WHERE cycle_id = %s", (cycle_id,))
    row = cur.fetchone()

    return SummaryResponse(
        id=row["id"],
        cycle_id=row["cycle_id"],
        content=row["content"],
        weighting_explanation=row["weighting_explanation"],
        finalised=bool(row["finalised"]),
        finalised_at=row["finalised_at"],
        updated_at=row["updated_at"]
    )


@router.post("/manager/{cycle_id}/generate", response_model=SummaryResponse)
def generate_summary_endpoint(cycle_id: int, db=Depends(get_db)):
    """Generate AI summary for the first time."""
    cur = db.cursor()

    # Check cycle exists
    cur.execute(
        """SELECT fc.id, u.name as subject_name
           FROM feedback_cycles fc
           JOIN users u ON fc.subject_user_id = u.id
           WHERE fc.id = %s""",
        (cycle_id,)
    )
    cycle = cur.fetchone()

    if not cycle:
        raise HTTPException(status_code=404, detail="Feedback cycle not found")

    # Check if summary already exists
    cur.execute("SELECT id FROM summaries WHERE cycle_id = %s", (cycle_id,))
    existing = cur.fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="Summary already exists. Use regenerate to replace it.")

    # Generate new summary
    return _generate_and_save_summary(cycle_id, cycle["subject_name"], db)


@router.post("/manager/{cycle_id}/regenerate", response_model=SummaryResponse)
def regenerate_summary(cycle_id: int, db=Depends(get_db)):
    """Regenerate AI summary (replaces existing)."""
    cur = db.cursor()

    # Check cycle exists
    cur.execute(
        """SELECT fc.id, u.name as subject_name
           FROM feedback_cycles fc
           JOIN users u ON fc.subject_user_id = u.id
           WHERE fc.id = %s""",
        (cycle_id,)
    )
    cycle = cur.fetchone()

    if not cycle:
        raise HTTPException(status_code=404, detail="Feedback cycle not found")

    # Check if finalised
    cur.execute("SELECT finalised FROM summaries WHERE cycle_id = %s", (cycle_id,))
    summary = cur.fetchone()

    if summary and summary["finalised"]:
        raise HTTPException(status_code=400, detail="Summary is finalised and cannot be regenerated")

    # Delete existing summary if present
    cur.execute("DELETE FROM summaries WHERE cycle_id = %s", (cycle_id,))
    db.commit()

    # Generate new summary
    return _generate_and_save_summary(cycle_id, cycle["subject_name"], db)


@router.post("/manager/{cycle_id}/finalise", response_model=SummaryResponse)
def finalise_summary(cycle_id: int, db=Depends(get_db)):
    """Lock summary - no further editing allowed."""
    cur = db.cursor()

    cur.execute("SELECT * FROM summaries WHERE cycle_id = %s", (cycle_id,))
    summary = cur.fetchone()

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    if summary["finalised"]:
        raise HTTPException(status_code=400, detail="Summary is already finalised")

    now = datetime.now()
    cur.execute(
        "UPDATE summaries SET finalised = TRUE, finalised_at = %s, updated_at = %s WHERE cycle_id = %s",
        (now, now, cycle_id)
    )
    db.commit()

    cur.execute("SELECT * FROM summaries WHERE cycle_id = %s", (cycle_id,))
    row = cur.fetchone()

    return SummaryResponse(
        id=row["id"],
        cycle_id=row["cycle_id"],
        content=row["content"],
        weighting_explanation=row["weighting_explanation"],
        finalised=bool(row["finalised"]),
        finalised_at=row["finalised_at"],
        updated_at=row["updated_at"]
    )


def _generate_and_save_summary(cycle_id: int, subject_name: str, db) -> SummaryResponse:
    """Generate AI summary and save to database."""
    cur = db.cursor()

    # Get all submitted reviews with reviewer info
    cur.execute(
        """SELECT rev.*, r.name as reviewer_name, r.relationship, r.frequency
           FROM reviews rev
           JOIN reviewers r ON rev.reviewer_id = r.id
           WHERE r.cycle_id = %s""",
        (cycle_id,)
    )
    reviews = cur.fetchall()

    if len(reviews) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 reviews are required to generate a summary"
        )

    # Generate summary using AI service
    content, weighting_explanation = generate_summary(
        employee_name=subject_name,
        reviews=[dict(r) for r in reviews]
    )

    # Save to database
    now = datetime.now()
    cur.execute(
        """INSERT INTO summaries (cycle_id, content, weighting_explanation, updated_at)
           VALUES (%s, %s, %s, %s) RETURNING *""",
        (cycle_id, content, weighting_explanation, now)
    )
    row = cur.fetchone()
    db.commit()

    return SummaryResponse(
        id=row["id"],
        cycle_id=row["cycle_id"],
        content=row["content"],
        weighting_explanation=row["weighting_explanation"],
        finalised=bool(row["finalised"]),
        finalised_at=row["finalised_at"],
        updated_at=row["updated_at"]
    )
