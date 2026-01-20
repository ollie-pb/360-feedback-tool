"""Employee API routes."""
import secrets
import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from app.database import get_db
from app.models import EmployeeCreate, EmployeeResponse, ReviewerCreate, ReviewerResponse

router = APIRouter()


@router.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: sqlite3.Connection = Depends(get_db)):
    """Create a new employee to start a review cycle."""
    cursor = db.execute(
        "INSERT INTO employees (name, email) VALUES (?, ?)",
        (employee.name, employee.email)
    )
    db.commit()

    employee_id = cursor.lastrowid
    row = db.execute(
        "SELECT id, name, email, created_at FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    return EmployeeResponse(
        id=row["id"],
        name=row["name"],
        email=row["email"],
        created_at=row["created_at"]
    )


@router.post("/employees/{employee_id}/reviewers", response_model=ReviewerResponse)
def add_reviewer(
    employee_id: int,
    reviewer: ReviewerCreate,
    db: sqlite3.Connection = Depends(get_db)
):
    """Add a reviewer to an employee's review cycle. Returns unique token."""
    # Verify employee exists
    employee = db.execute(
        "SELECT id FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check for duplicate reviewer email for this employee
    existing = db.execute(
        "SELECT id FROM reviewers WHERE employee_id = ? AND email = ?",
        (employee_id, reviewer.email)
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="This reviewer has already been added for this employee"
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

    cursor = db.execute(
        """INSERT INTO reviewers (employee_id, name, email, relationship, frequency, token)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (employee_id, reviewer.name, reviewer.email, reviewer.relationship, reviewer.frequency, token)
    )
    db.commit()

    reviewer_id = cursor.lastrowid
    row = db.execute(
        "SELECT * FROM reviewers WHERE id = ?",
        (reviewer_id,)
    ).fetchone()

    return ReviewerResponse(
        id=row["id"],
        employee_id=row["employee_id"],
        name=row["name"],
        email=row["email"],
        relationship=row["relationship"],
        frequency=row["frequency"],
        token=row["token"],
        created_at=row["created_at"],
        has_submitted=False
    )
