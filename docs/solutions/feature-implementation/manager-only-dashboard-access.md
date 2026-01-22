---
title: "Manager-Only Dashboard Access for 360 Feedback Tool"
category: "feature-implementation"
tags:
  - fastapi
  - postgresql
  - role-based-access
  - 360-feedback
  - privacy
  - dashboard
  - user-permissions
components:
  - app/database.py
  - app/models.py
  - app/routes/cycles.py
  - app/routes/manager.py
  - app/routes/auth.py
  - static/nominate.html
  - static/dashboard.html
  - static/manager.html
severity: medium
date_solved: "2026-01-22"
---

# Manager-Only Dashboard Access for 360 Feedback Tool

## Problem

The 360 Feedback Tool allowed subjects (employees being reviewed) to see the full feedback cycle dashboard, including:
- Who submitted feedback
- Raw AI summaries before manager review
- Individual reviewer details and status

This defeats the purpose of 360 feedback where the manager should synthesize and present feedback to the employee.

### Symptoms

- Subjects could navigate directly to `/cycle/{id}` and see everything
- Dashboard showed "View Cycle" button for subjects' own cycles
- No distinction between subject and manager views

### Impact

- Reviewers might be less honest knowing subjects could identify who submitted what
- Subjects could read unfiltered AI summaries before manager context was added
- Undermined trust in the 360 feedback process

## Root Cause

No role-based access control distinguishing between manager and subject views. The system only tracked `subject_user_id` and `created_by_user_id` - no manager relationship existed.

## Solution

Implement manager-user relationship and role-based dashboard rendering.

### 1. Database Schema Change

Added `manager_user_id` column to `feedback_cycles` table:

```sql
ALTER TABLE feedback_cycles ADD COLUMN manager_user_id INTEGER REFERENCES users(id);
CREATE INDEX IF NOT EXISTS idx_feedback_cycles_manager ON feedback_cycles(manager_user_id);
```

### 2. Backend Model Updates

**CycleCreate** - Now requires manager info:

```python
class CycleCreate(BaseModel):
    name: str
    email: str
    title: Optional[str] = None
    manager_name: str      # NEW
    manager_email: str     # NEW
```

**UserDashboard** - Includes managed cycles:

```python
class UserDashboard(BaseModel):
    user: UserResponse
    my_cycles: list[DashboardCycle]       # Where user is subject
    managed_cycles: list[DashboardCycle]  # Where user is manager (NEW)
    pending_reviews: list[InboxItem]
```

**ManagerDashboard** - Returns role detection fields:

```python
class ManagerDashboard(BaseModel):
    employee: EmployeeResponse
    subject_email: Optional[str] = None   # For frontend role detection (NEW)
    manager_name: Optional[str] = None    # NEW
    manager_email: Optional[str] = None   # NEW
    reviewers: list[ReviewerWithStatus]
    summary: Optional[SummaryResponse]
    submitted_count: int
    total_reviewers: int
```

### 3. Cycle Creation Links Manager

```python
# Get or create manager user
manager_user = get_or_create_user(cycle.manager_email, cycle.manager_name)
manager_user_id = manager_user["id"]

# Create cycle with manager link
cur.execute(
    """INSERT INTO feedback_cycles (subject_user_id, created_by_user_id, manager_user_id, title)
       VALUES (%s, %s, %s, %s) RETURNING *""",
    (subject_user_id, created_by_user_id, manager_user_id, cycle.title)
)
```

### 4. Dashboard Returns Managed Cycles

```python
# Get cycles where user is the manager
cur.execute(
    """SELECT fc.id, fc.title, fc.status, ...
       FROM feedback_cycles fc
       JOIN users u ON fc.subject_user_id = u.id
       LEFT JOIN users m ON fc.manager_user_id = m.id
       WHERE fc.manager_user_id = %s
       ORDER BY fc.created_at DESC""",
    (user["id"],)
)
managed_cycles = [...]
```

### 5. Frontend Role-Based Rendering

**Cycle page** checks user role:

```javascript
const isSubject = user && user.email === data.subject_email;

if (isSubject) {
    renderSubjectView(data);  // Limited progress view
} else {
    renderManagerView(data);  // Full dashboard
}
```

**Subject view** shows limited info:

```javascript
function renderSubjectView(data) {
    document.getElementById('dashboard').innerHTML = `
        <h1>Your Feedback Cycle</h1>
        <div class="card">
            <h3>Collection Progress</h3>
            <p><strong>${data.submitted_count} of ${data.total_reviewers}</strong> reviewers have submitted feedback</p>
            <progress value="${data.submitted_count}" max="${data.total_reviewers}"></progress>
        </div>
        <div class="message info">
            <p>Your manager <strong>${data.manager_name}</strong> will review this feedback and discuss it with you.</p>
        </div>
    `;
}
```

**Dashboard** shows managed cycles with view button:

```javascript
// Managed cycles section (managers only)
managedContainer.innerHTML = data.managed_cycles.map(cycle => `
    <div class="card">
        <h3>${cycle.title || 'Feedback Cycle'}</h3>
        <p><strong>Employee:</strong> ${cycle.subject_name}</p>
        <p><strong>Progress:</strong> ${cycle.submitted_count} of ${cycle.total_reviewers}</p>
        <a href="/cycle/${cycle.id}"><button class="secondary">View & Review Feedback</button></a>
    </div>
`).join('');

// My cycles section (subjects - no view button)
cyclesContainer.innerHTML = data.my_cycles.map(cycle => `
    <div class="card">
        <h3>${cycle.title || 'Feedback Cycle'}</h3>
        <p><strong>Progress:</strong> ${cycle.submitted_count} of ${cycle.total_reviewers}</p>
        <p><strong>Manager:</strong> ${cycle.manager_name || 'Not assigned'}</p>
    </div>
`).join('');
```

## Role-Based Access Summary

| Feature | Subject | Manager |
|---------|---------|---------|
| Progress count (X of Y) | Yes | Yes |
| Reviewer names | No | Yes |
| Reviewer submission status | No | Yes |
| AI Summary content | No | Yes |
| Edit Summary | No | Yes |
| Regenerate Summary | No | Yes |
| Finalize Summary | No | Yes |
| View Cycle button on dashboard | No | Yes |

## Prevention

1. **Always design with roles in mind** - When building dashboards that show sensitive data, identify who should see what upfront
2. **Return role-detection fields** - Include enough data in API responses for frontend to make rendering decisions
3. **Frontend checks are UX, not security** - Note that this implementation is UX-only. For true security, backend should enforce access control

## Related Documentation

- [plans/manager-only-dashboard-access.md](../../../plans/manager-only-dashboard-access.md) - Original implementation plan
- [MVP PRD.md](../../../MVP%20PRD.md) - Manager Dashboard section
- [feedback-tool-improvements.md](../../../plans/feedback-tool-improvements.md) - User system that enables role-based access

## Files Modified

| File | Change |
|------|--------|
| `app/database.py` | Added `manager_user_id` column |
| `app/models.py` | Updated CycleCreate, CycleResponse, DashboardCycle, ManagerDashboard, UserDashboard |
| `app/routes/cycles.py` | Create manager user and link to cycle |
| `app/routes/manager.py` | Return subject_email, manager_name, manager_email |
| `app/routes/auth.py` | Return manager_name and managed_cycles |
| `static/nominate.html` | Manager name/email fields, updated success message |
| `static/dashboard.html` | Managed cycles section, removed View button from own cycles |
| `static/manager.html` | Role-based rendering (subject vs manager view) |
