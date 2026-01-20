# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

360 Feedback Summarisation Tool - a prototype for collecting structured 360-degree feedback, weighting it by relationship/frequency, and generating AI summaries for managers.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Static HTML/JS (no build step)
- **Database**: SQLite
- **AI**: Claude API (claude-sonnet-4-5-20250514)

## Architecture

Four user flows connecting through a central system:

1. **Employee** → nominates 3-6 reviewers with relationship type + collaboration frequency
2. **Reviewer** → submits structured feedback (start/stop/continue doing + example) via unique token link
3. **System** → when 2+ reviews exist, generates weighted summary using Claude API
4. **Manager** → views progress, edits summary, finalises

### Weighting Logic

Combined weight = relationship_weight × frequency_weight

- Relationship: Manager (1.0) > Peer (0.8) > Direct Report (0.7) > Cross-functional (0.6)
- Frequency: Weekly (1.0) > Monthly (0.7) > Rarely (0.4)

### Data Model

`employees` → `reviewers` (with token) → `reviews` (feedback fields)
`employees` → `summaries` (generated content, finalised flag)

## API Structure

All routes under `/api/`:
- Employee management: `POST /employees`, `POST /employees/{id}/reviewers`
- Reviewer actions: `GET /review/{token}`, `POST /review/{token}`
- Inbox: `GET /inbox/{email}`
- Manager dashboard: `GET /manager/{employee_id}`, `PUT /manager/{employee_id}/summary`, `POST /manager/{employee_id}/finalise`

## Development Notes

- MVP timebox: 6 hours - prioritise happy-path over edge cases
- No auth required
- Pre-seed test data for demo (employee "Alex Chen" with 4 reviewers, 3 submitted)
- Summary auto-generates at 2+ submitted reviews
