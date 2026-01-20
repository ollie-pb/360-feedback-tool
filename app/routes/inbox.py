"""Reviewer inbox API routes."""
import sqlite3
from fastapi import APIRouter, Depends

from app.database import get_db
from app.models import InboxItem

router = APIRouter()


@router.get("/inbox/{email}", response_model=list[InboxItem])
def get_inbox(email: str, db: sqlite3.Connection = Depends(get_db)):
    """List all pending and submitted reviews for a reviewer email."""
    rows = db.execute(
        """SELECT r.id, r.employee_id, r.relationship, r.frequency, r.token, e.name as employee_name,
                  (SELECT COUNT(*) FROM reviews WHERE reviewer_id = r.id) as has_review
           FROM reviewers r
           JOIN employees e ON r.employee_id = e.id
           WHERE r.email = ?
           ORDER BY r.created_at DESC""",
        (email,)
    ).fetchall()

    return [
        InboxItem(
            employee_name=row["employee_name"],
            employee_id=row["employee_id"],
            relationship=row["relationship"],
            frequency=row["frequency"],
            token=row["token"],
            status="submitted" if row["has_review"] > 0 else "pending"
        )
        for row in rows
    ]
