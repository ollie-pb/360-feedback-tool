---
title: "Auto-Regenerate AI Summary on Review Submission"
category: "feature-implementation"
tags:
  - fastapi
  - background-tasks
  - async-processing
  - claude-api
  - 360-feedback
  - summarisation
components:
  - app/routes/review.py
  - app/services/summarisation.py
severity: medium
date_solved: "2026-01-22"
---

# Auto-Regenerate AI Summary on Review Submission

## Problem Statement

Managers viewing 360 feedback summaries saw stale data because summaries were only generated on-demand when clicking "Generate Summary". This created two issues:

1. **Stale summaries**: Managers viewed outdated summaries that didn't include recent feedback
2. **Manual effort**: Managers had to remember to regenerate after new reviews arrived

## Solution

Use FastAPI's built-in `BackgroundTasks` to trigger summary regeneration automatically after each review submission.

### How It Works

```
Review Submitted (POST /api/review/{token})
       │
       ▼
┌─────────────────────────────────────┐
│  1. Validate token                  │
│  2. Save review to database         │
│  3. Trigger background task         │
│  4. Return 200 immediately          │
└─────────────────────────────────────┘
       │
       ▼ (async, after response sent)
┌─────────────────────────────────────┐
│  Background Task                    │
│  1. Check review count >= 2         │
│  2. Check summary not finalised     │
│  3. Call Claude API                 │
│  4. Save/update summary             │
└─────────────────────────────────────┘
```

### Implementation

**1. Modified review submission endpoint (`app/routes/review.py`):**

```python
from fastapi import BackgroundTasks
from app.services.summarisation import regenerate_summary_for_cycle

@router.post("/review/{token}", response_model=ReviewResponse)
def submit_review(
    token: str,
    review: ReviewSubmit,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    # ... existing validation and insert logic ...

    # Get cycle_id from reviewer
    cur.execute("SELECT id, cycle_id FROM reviewers WHERE token = %s", (token,))
    reviewer = cur.fetchone()

    # ... save review ...
    db.commit()

    # Trigger summary regeneration in background
    background_tasks.add_task(regenerate_summary_for_cycle, reviewer["cycle_id"])

    return ReviewResponse(...)
```

**2. New background task function (`app/services/summarisation.py`):**

```python
def regenerate_summary_for_cycle(cycle_id: int):
    """
    Background task to regenerate summary after review submission.

    Conditions:
    - At least 2 reviews must exist
    - Summary must NOT be finalised
    """
    conn = get_connection()
    cur = conn.cursor()

    # Check review count
    review_count = ...  # query count
    if review_count < 2:
        return  # Skip if below threshold

    # Check if summary is finalised
    existing_summary = ...  # query summary
    if existing_summary and existing_summary["finalised"]:
        return  # Skip if finalised (protected)

    # Generate and save summary
    summary_content, weighting_explanation = generate_summary(subject_name, reviews)

    # Insert or update summary
    if existing_summary:
        cur.execute("UPDATE summaries SET content = %s ...", ...)
    else:
        cur.execute("INSERT INTO summaries ...", ...)

    conn.commit()
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **FastAPI BackgroundTasks** | Built-in, no new dependencies, suitable for I/O-bound tasks |
| **No retry logic** | MVP simplicity; next review submission triggers fresh attempt |
| **Silent error handling** | Errors logged but don't block review submission |
| **Finalised protection** | Finalised summaries never overwritten by auto-regeneration |
| **2+ review threshold** | Matches existing business rule for summary generation |

## Edge Cases Handled

1. **First review**: Background task runs but exits early (< 2 reviews)
2. **Finalised summary**: Background task detects and skips (no overwrite)
3. **Claude API failure**: Error logged, existing summary unchanged
4. **Rapid submissions**: Eventual consistency accepted (last writer wins)

## Testing

Manual test scenarios:

1. Submit 2nd review → verify summary auto-generates
2. Submit 3rd+ review → verify summary updates
3. Finalise summary, submit new review → verify summary unchanged
4. Break API key temporarily → verify review saves, error logged

## Prevention & Future Considerations

For production scale, consider:

- **Debouncing**: Batch rapid submissions within time window
- **Distributed locking**: Prevent duplicate API calls
- **Status tracking**: Add "generating" state for UI feedback
- **Retry logic**: Automatic retry with exponential backoff

## Related Documentation

- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- Plan: `plans/feat-auto-regenerate-summary-on-review-submission.md`

## Files Modified

- `app/routes/review.py` - Added BackgroundTasks trigger
- `app/services/summarisation.py` - Added `regenerate_summary_for_cycle()` function
