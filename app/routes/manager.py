"""Manager dashboard API routes."""
import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from app.database import get_db
from app.models import (
    EmployeeResponse, ReviewerWithStatus, SummaryResponse,
    SummaryUpdate, ManagerDashboard
)
from app.services.summarisation import generate_summary

router = APIRouter()


@router.get("/manager/{employee_identifier}", response_model=ManagerDashboard)
def get_manager_dashboard(employee_identifier: str, db: sqlite3.Connection = Depends(get_db)):
    """Get manager dashboard with reviewers, statuses, and summary."""
    # Get employee - support lookup by ID or name
    # Try as integer ID first
    try:
        employee_id = int(employee_identifier)
        employee = db.execute(
            "SELECT id, name, email, created_at FROM employees WHERE id = ?",
            (employee_id,)
        ).fetchone()
    except ValueError:
        # Not an integer, try name lookup
        employee = db.execute(
            "SELECT id, name, email, created_at FROM employees WHERE name = ?",
            (employee_identifier,)
        ).fetchone()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_id = employee["id"]

    # Get reviewers with status
    reviewers = db.execute(
        """SELECT r.id, r.name, r.email, r.relationship, r.frequency,
                  (SELECT COUNT(*) FROM reviews WHERE reviewer_id = r.id) as has_review
           FROM reviewers r
           WHERE r.employee_id = ?
           ORDER BY r.created_at""",
        (employee_id,)
    ).fetchall()

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

    # Get or generate summary
    summary = db.execute(
        "SELECT * FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    summary_response = None
    if summary:
        summary_response = SummaryResponse(
            id=summary["id"],
            employee_id=summary["employee_id"],
            content=summary["content"],
            weighting_explanation=summary["weighting_explanation"],
            finalised=bool(summary["finalised"]),
            finalised_at=summary["finalised_at"],
            updated_at=summary["updated_at"]
        )
    # Note: Summary is NOT auto-generated. Manager must click "Generate Summary" button.

    return ManagerDashboard(
        employee=EmployeeResponse(
            id=employee["id"],
            name=employee["name"],
            email=employee["email"],
            created_at=employee["created_at"]
        ),
        reviewers=reviewers_list,
        summary=summary_response,
        submitted_count=submitted_count,
        total_reviewers=len(reviewers_list)
    )


@router.put("/manager/{employee_id}/summary", response_model=SummaryResponse)
def update_summary(
    employee_id: int,
    update: SummaryUpdate,
    db: sqlite3.Connection = Depends(get_db)
):
    """Edit summary content."""
    # Check if summary exists
    summary = db.execute(
        "SELECT * FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    if summary["finalised"]:
        raise HTTPException(status_code=400, detail="Summary is finalised and cannot be edited")

    # Update summary
    db.execute(
        "UPDATE summaries SET content = ?, updated_at = ? WHERE employee_id = ?",
        (update.content, datetime.now().isoformat(), employee_id)
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    return SummaryResponse(
        id=row["id"],
        employee_id=row["employee_id"],
        content=row["content"],
        weighting_explanation=row["weighting_explanation"],
        finalised=bool(row["finalised"]),
        finalised_at=row["finalised_at"],
        updated_at=row["updated_at"]
    )


@router.post("/manager/{employee_id}/generate", response_model=SummaryResponse)
def generate_summary_endpoint(employee_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Generate AI summary for the first time."""
    # Check employee exists
    employee = db.execute(
        "SELECT id FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if summary already exists
    existing = db.execute(
        "SELECT id FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="Summary already exists. Use regenerate to replace it.")

    # Generate new summary
    return _generate_and_save_summary(employee_id, db)


@router.post("/manager/{employee_id}/regenerate", response_model=SummaryResponse)
def regenerate_summary(employee_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Regenerate AI summary (replaces existing)."""
    # Check employee exists
    employee = db.execute(
        "SELECT id FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if finalised
    summary = db.execute(
        "SELECT finalised FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    if summary and summary["finalised"]:
        raise HTTPException(status_code=400, detail="Summary is finalised and cannot be regenerated")

    # Delete existing summary if present
    db.execute("DELETE FROM summaries WHERE employee_id = ?", (employee_id,))
    db.commit()

    # Generate new summary
    return _generate_and_save_summary(employee_id, db)


@router.post("/manager/{employee_id}/finalise", response_model=SummaryResponse)
def finalise_summary(employee_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Lock summary - no further editing allowed."""
    summary = db.execute(
        "SELECT * FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    if summary["finalised"]:
        raise HTTPException(status_code=400, detail="Summary is already finalised")

    now = datetime.now().isoformat()
    db.execute(
        "UPDATE summaries SET finalised = TRUE, finalised_at = ?, updated_at = ? WHERE employee_id = ?",
        (now, now, employee_id)
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    return SummaryResponse(
        id=row["id"],
        employee_id=row["employee_id"],
        content=row["content"],
        weighting_explanation=row["weighting_explanation"],
        finalised=bool(row["finalised"]),
        finalised_at=row["finalised_at"],
        updated_at=row["updated_at"]
    )


def _generate_and_save_summary(employee_id: int, db: sqlite3.Connection) -> SummaryResponse:
    """Generate AI summary and save to database."""
    # Get employee name
    employee = db.execute(
        "SELECT name FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    # Get all submitted reviews with reviewer info
    reviews = db.execute(
        """SELECT rev.*, r.name as reviewer_name, r.relationship, r.frequency
           FROM reviews rev
           JOIN reviewers r ON rev.reviewer_id = r.id
           WHERE r.employee_id = ?""",
        (employee_id,)
    ).fetchall()

    if len(reviews) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 reviews are required to generate a summary"
        )

    # Generate summary using AI service
    content, weighting_explanation = generate_summary(
        employee_name=employee["name"],
        reviews=[dict(r) for r in reviews]
    )

    # Save to database
    now = datetime.now().isoformat()
    db.execute(
        """INSERT INTO summaries (employee_id, content, weighting_explanation, updated_at)
           VALUES (?, ?, ?, ?)""",
        (employee_id, content, weighting_explanation, now)
    )
    db.commit()

    row = db.execute(
        "SELECT * FROM summaries WHERE employee_id = ?",
        (employee_id,)
    ).fetchone()

    return SummaryResponse(
        id=row["id"],
        employee_id=row["employee_id"],
        content=row["content"],
        weighting_explanation=row["weighting_explanation"],
        finalised=bool(row["finalised"]),
        finalised_at=row["finalised_at"],
        updated_at=row["updated_at"]
    )
