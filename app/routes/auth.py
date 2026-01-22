"""User authentication and dashboard API routes."""
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db, get_or_create_user
from app.models import (
    LoginRequest, UserResponse, UserDashboard,
    DashboardCycle, InboxItem
)

router = APIRouter()


@router.post("/auth/login", response_model=UserResponse)
def login(request: LoginRequest, db=Depends(get_db)):
    """Login or create user with email. No password for MVP."""
    user = get_or_create_user(request.email, request.name)

    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        is_demo=user["is_demo"],
        created_at=user["created_at"]
    )


@router.get("/auth/dashboard/{email}", response_model=UserDashboard)
def get_dashboard(email: str, db=Depends(get_db)):
    """Get user's personal dashboard with their cycles and pending reviews."""
    cur = db.cursor()

    # Get user
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get cycles where user is the subject
    cur.execute(
        """SELECT fc.id, fc.title, fc.status, fc.created_at, u.name as subject_name,
                  (SELECT COUNT(*) FROM reviewers r WHERE r.cycle_id = fc.id) as total_reviewers,
                  (SELECT COUNT(*) FROM reviewers r
                   JOIN reviews rev ON r.id = rev.reviewer_id
                   WHERE r.cycle_id = fc.id) as submitted_count
           FROM feedback_cycles fc
           JOIN users u ON fc.subject_user_id = u.id
           WHERE fc.subject_user_id = %s
           ORDER BY fc.created_at DESC""",
        (user["id"],)
    )
    my_cycles = [
        DashboardCycle(
            id=row["id"],
            title=row["title"],
            subject_name=row["subject_name"],
            status=row["status"],
            submitted_count=row["submitted_count"],
            total_reviewers=row["total_reviewers"],
            created_at=row["created_at"]
        )
        for row in cur.fetchall()
    ]

    # Get cycles where user is the manager
    cur.execute(
        """SELECT fc.id, fc.title, fc.status, fc.created_at, u.name as subject_name,
                  (SELECT COUNT(*) FROM reviewers r WHERE r.cycle_id = fc.id) as total_reviewers,
                  (SELECT COUNT(*) FROM reviewers r
                   JOIN reviews rev ON r.id = rev.reviewer_id
                   WHERE r.cycle_id = fc.id) as submitted_count
           FROM feedback_cycles fc
           JOIN users u ON fc.subject_user_id = u.id
           WHERE fc.manager_user_id = %s
           ORDER BY fc.created_at DESC""",
        (user["id"],)
    )
    cycles_to_manage = [
        DashboardCycle(
            id=row["id"],
            title=row["title"],
            subject_name=row["subject_name"],
            status=row["status"],
            submitted_count=row["submitted_count"],
            total_reviewers=row["total_reviewers"],
            created_at=row["created_at"]
        )
        for row in cur.fetchall()
    ]

    # Get pending reviews (where user is a reviewer)
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
    pending_reviews = [
        InboxItem(
            employee_name=row["employee_name"],
            cycle_id=row["cycle_id"],
            relationship=row["relationship"],
            frequency=row["frequency"],
            token=row["token"],
            status="submitted" if row["has_review"] > 0 else "pending"
        )
        for row in cur.fetchall()
    ]

    return UserDashboard(
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            is_demo=user["is_demo"],
            created_at=user["created_at"]
        ),
        my_cycles=my_cycles,
        cycles_to_manage=cycles_to_manage,
        pending_reviews=pending_reviews
    )
