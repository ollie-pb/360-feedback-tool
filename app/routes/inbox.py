"""Reviewer inbox API routes."""
from fastapi import APIRouter, Depends

from app.database import get_db
from app.models import InboxItem

router = APIRouter()


@router.get("/inbox/{email}", response_model=list[InboxItem])
def get_inbox(email: str, db=Depends(get_db)):
    """List all pending and submitted reviews for a reviewer email."""
    cur = db.cursor()

    cur.execute(
        """SELECT r.id, r.cycle_id, r.relationship, r.frequency, r.token,
                  u.name as employee_name,
                  (SELECT COUNT(*) FROM reviews WHERE reviewer_id = r.id) as has_review
           FROM reviewers r
           JOIN feedback_cycles fc ON r.cycle_id = fc.id
           JOIN users u ON fc.subject_user_id = u.id
           WHERE r.email = %s
           ORDER BY r.created_at DESC""",
        (email,)
    )
    rows = cur.fetchall()

    return [
        InboxItem(
            employee_name=row["employee_name"],
            cycle_id=row["cycle_id"],
            relationship=row["relationship"],
            frequency=row["frequency"],
            token=row["token"],
            status="submitted" if row["has_review"] > 0 else "pending"
        )
        for row in rows
    ]
