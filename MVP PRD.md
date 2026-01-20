# 360 Feedback Summarisation Tool - MVP Spec

## Overview

A lightweight prototype to improve the quality and efficiency of 360-degree feedback collection. Employees nominate reviewers, reviewers submit structured feedback, and managers view weighted AI-generated summaries.

**Timebox**: 6 hours  
**Priority**: Working happy-path > polish/edge cases

---

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | Static HTML/JS | Simple, no build step |
| Backend | FastAPI (Python) | Lightweight, good Claude SDK support |
| Database | SQLite | Reliable for demo, easy to seed test data |
| AI | Claude API (claude-sonnet-4-5-20250514) | Summarisation + weighting |

---

## Data Model

### employees
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| name | TEXT | Employee being reviewed |
| email | TEXT | For display only |
| created_at | TIMESTAMP | |

### reviewers
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| employee_id | INTEGER | FK → employees |
| name | TEXT | Reviewer's name |
| email | TEXT | For inbox lookup |
| relationship | TEXT | manager / peer / direct_report / xfn |
| frequency | TEXT | weekly / monthly / rarely |
| token | TEXT | Unique link token (UUID) |
| created_at | TIMESTAMP | |

### reviews
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| reviewer_id | INTEGER | FK → reviewers |
| start_doing | TEXT | Feedback field |
| stop_doing | TEXT | Feedback field |
| continue_doing | TEXT | Feedback field |
| example | TEXT | Required example prompt |
| additional | TEXT | Optional free-text |
| submitted_at | TIMESTAMP | NULL = pending |

### summaries
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| employee_id | INTEGER | FK → employees |
| content | TEXT | Generated/edited summary (markdown) |
| weighting_explanation | TEXT | Brief explanation of weights used |
| finalised | BOOLEAN | Locks editing when true |
| finalised_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

---

## API Routes

| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/api/employees` | Create employee + start review cycle |
| POST | `/api/employees/{id}/reviewers` | Add reviewer, returns unique token |
| GET | `/api/review/{token}` | Get context for review form (employee name, relationship) |
| POST | `/api/review/{token}` | Submit feedback |
| GET | `/api/inbox/{email}` | List all pending reviews for a reviewer |
| GET | `/api/manager/{employee_id}` | Get reviewers, statuses, and summary |
| PUT | `/api/manager/{employee_id}/summary` | Edit summary content |
| POST | `/api/manager/{employee_id}/finalise` | Lock summary |

---

## Pages

### 1. `/nominate` - Employee nominates reviewers
**User**: Employee

- Input employee name + email
- Add 3-6 reviewers, each with:
  - Name
  - Relationship type (dropdown): Manager / Peer / Direct Report / Cross-functional
  - Collaboration frequency (dropdown): Weekly / Monthly / Rarely
- Submit generates unique review links
- Display links to copy/share (no email send)

### 2. `/review/{token}` - Reviewer submits feedback
**User**: Reviewer

- Shows: "You're reviewing [Employee Name]"
- Form fields:
  - **Start doing**: What should they start doing?
  - **Stop doing**: What should they stop doing?
  - **Continue doing**: What should they keep doing?
  - **Example** (required): "Describe a specific moment you observed this person demonstrating a strength or area for growth"
  - **Additional comments** (optional): Free-text
- Submit button → confirmation message

### 3. `/inbox/{email}` - Reviewer inbox (efficiency feature)
**User**: Reviewer

- Shows all pending reviews for this email address
- List view with:
  - Employee name
  - Relationship type
  - Status: Pending / Submitted
  - Link to complete (if pending)
- Allows quick completion of multiple reviews

### 4. `/manager/{employee_id}` - Manager dashboard
**User**: Manager

- **Reviewer progress table**:
  - Name | Relationship | Frequency | Status (Pending/Submitted)
- **Summary section** (appears when 2+ reviews submitted):
  - Auto-generated summary with sections:
    - Strengths
    - Growth Areas
    - Key Examples
    - Suggested Focus
  - Weighting explanation (collapsible/subtle)
  - Editable text area
  - "Regenerate" button (re-runs AI)
- **Finalise button**:
  - Locks summary
  - Shows final read-only view

---

## Summarisation Logic

### Trigger
Generate summary when `submitted_reviews >= 2`

### Weighting Factors

**Relationship weight**:
| Type | Weight |
|------|--------|
| Manager | 1.0 |
| Peer | 0.8 |
| Direct Report | 0.7 |
| Cross-functional | 0.6 |

**Frequency weight**:
| Frequency | Weight |
|-----------|--------|
| Weekly | 1.0 |
| Monthly | 0.7 |
| Rarely | 0.4 |

**Combined weight** = relationship_weight × frequency_weight

### Prompt (Claude API)

```
You are summarising 360-degree feedback for an employee performance review.

## Feedback Submissions
{for each review, include}
- Reviewer: {name} ({relationship}, works together {frequency})
- Weight: {combined_weight} (based on relationship and collaboration frequency)
- Start doing: {start_doing}
- Stop doing: {stop_doing}
- Continue doing: {continue_doing}
- Example: {example}
- Additional: {additional}

## Instructions
Synthesise this feedback into a summary with these sections:
1. **Strengths** - What this person does well (weight higher-confidence feedback more heavily)
2. **Growth Areas** - Where they can improve
3. **Key Examples** - Specific behaviours observed (quote or paraphrase from feedback)
4. **Suggested Focus** - 1-2 priority areas for development

Weight feedback from managers and frequent collaborators more heavily than occasional cross-functional contacts.

Keep the tone constructive and actionable. Be concise.
```

### Weighting Explanation (auto-generated)
Display beneath summary:
> "This summary weights feedback based on reviewer relationship (manager feedback weighted highest) and collaboration frequency (weekly interactions weighted highest). [Manager Name]'s feedback as a manager with weekly interaction carried the most weight."

---

## Out of Scope (Explicitly)

- Authentication / login
- Email sending
- Multiple review cycles
- Edge case handling
- Responsive design / styling polish
- PDF export
- Reminder nudges
- Audio input

---

## Test Data (Pre-seed)

For demo reliability, seed database with:

**Employee**: Alex Chen

**Reviewers**:
| Name | Relationship | Frequency | Status |
|------|--------------|-----------|--------|
| Sam Taylor | Manager | Weekly | Submitted |
| Jordan Lee | Peer | Weekly | Submitted |
| Casey Morgan | Direct Report | Monthly | Submitted |
| Riley Kumar | Cross-functional | Rarely | Pending |

This ensures summary generation works immediately in demo.

---

## Demo Flow (2-3 min)

1. **Employee view** (30s): Show nominating a new reviewer, copy link
2. **Reviewer inbox** (30s): Show inbox with multiple pending, complete one quickly
3. **Reviewer form** (30s): Submit structured feedback
4. **Manager dashboard** (60s): Show progress, view weighted summary, explain weighting, edit, finalise

---

## Success Criteria

- [ ] Employee can add 3-6 reviewers with relationship + frequency
- [ ] Unique review links generated
- [ ] Reviewer can submit structured feedback via form
- [ ] Reviewer inbox shows all pending reviews for an email
- [ ] Manager sees reviewer list with status
- [ ] Summary auto-generates when 2+ reviews exist
- [ ] Summary grouped into 4 sections
- [ ] Weighting applied and explained
- [ ] Manager can edit summary
- [ ] Finalise locks the summary