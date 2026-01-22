"""Pydantic models for request/response validation."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# User models
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_demo: bool
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    name: str


# Feedback Cycle models (replaces Employee)
class CycleCreate(BaseModel):
    name: str  # Subject's name (for display)
    email: str  # Subject's email
    title: Optional[str] = None  # e.g., "Q4 2024 Review"
    manager_name: str  # Manager who will review the feedback
    manager_email: str  # Manager's email


class CycleResponse(BaseModel):
    id: int
    subject_user_id: int
    created_by_user_id: int
    manager_user_id: Optional[int] = None
    title: Optional[str]
    status: str
    created_at: datetime
    subject_name: Optional[str] = None  # Populated from join
    manager_name: Optional[str] = None  # Populated from join
    manager_email: Optional[str] = None  # Populated from join


# Reviewer models
class ReviewerCreate(BaseModel):
    name: str
    email: str
    relationship: str  # manager, peer, direct_report, xfn
    frequency: str  # weekly, monthly, rarely


class ReviewerResponse(BaseModel):
    id: int
    cycle_id: int
    name: str
    email: str
    relationship: str
    frequency: str
    token: str
    created_at: datetime
    has_submitted: bool = False


class ReviewerWithStatus(BaseModel):
    id: int
    name: str
    email: str
    relationship: str
    frequency: str
    status: str  # pending or submitted


# Review models
class ReviewContext(BaseModel):
    employee_name: str  # Subject of the feedback cycle
    relationship: str
    reviewer_name: str
    already_submitted: bool = False


class ReviewSubmit(BaseModel):
    start_doing: str
    stop_doing: str
    continue_doing: str
    example: str
    additional: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    reviewer_id: int
    start_doing: str
    stop_doing: str
    continue_doing: str
    example: str
    additional: Optional[str]
    submitted_at: datetime


# Inbox models
class InboxItem(BaseModel):
    employee_name: str  # Subject of the feedback cycle
    cycle_id: int
    relationship: str
    frequency: str
    token: str
    status: str  # pending or submitted


# Dashboard models
class SummaryResponse(BaseModel):
    id: int
    cycle_id: int
    content: str
    weighting_explanation: Optional[str]
    finalised: bool
    finalised_at: Optional[datetime]
    updated_at: datetime


class SummaryUpdate(BaseModel):
    content: str


class CycleDashboard(BaseModel):
    """Dashboard view for a feedback cycle."""
    cycle: CycleResponse
    subject_name: str
    reviewers: list[ReviewerWithStatus]
    summary: Optional[SummaryResponse]
    submitted_count: int
    total_reviewers: int


# User dashboard models
class DashboardCycle(BaseModel):
    """Summary of a feedback cycle for dashboard display."""
    id: int
    title: Optional[str]
    subject_name: str
    manager_name: Optional[str] = None
    status: str
    submitted_count: int
    total_reviewers: int
    created_at: datetime


class UserDashboard(BaseModel):
    """User's personal dashboard."""
    user: UserResponse
    my_cycles: list[DashboardCycle]  # Cycles where user is the subject
    managed_cycles: list[DashboardCycle]  # Cycles where user is the manager
    pending_reviews: list[InboxItem]  # Reviews user needs to complete


# Legacy compatibility (to be removed)
class EmployeeCreate(BaseModel):
    name: str
    email: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class ManagerDashboard(BaseModel):
    employee: EmployeeResponse
    subject_email: Optional[str] = None
    manager_name: Optional[str] = None
    manager_email: Optional[str] = None
    reviewers: list[ReviewerWithStatus]
    summary: Optional[SummaryResponse]
    submitted_count: int
    total_reviewers: int
