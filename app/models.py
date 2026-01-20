"""Pydantic models for request/response validation."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Employee models
class EmployeeCreate(BaseModel):
    name: str
    email: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


# Reviewer models
class ReviewerCreate(BaseModel):
    name: str
    email: str
    relationship: str  # manager, peer, direct_report, xfn
    frequency: str  # weekly, monthly, rarely


class ReviewerResponse(BaseModel):
    id: int
    employee_id: int
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
    employee_name: str
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
    employee_name: str
    employee_id: int
    relationship: str
    frequency: str
    token: str
    status: str  # pending or submitted


# Manager dashboard models
class SummaryResponse(BaseModel):
    id: int
    employee_id: int
    content: str
    weighting_explanation: Optional[str]
    finalised: bool
    finalised_at: Optional[datetime]
    updated_at: datetime


class SummaryUpdate(BaseModel):
    content: str


class ManagerDashboard(BaseModel):
    employee: EmployeeResponse
    reviewers: list[ReviewerWithStatus]
    summary: Optional[SummaryResponse]
    submitted_count: int
    total_reviewers: int
