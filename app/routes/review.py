"""Review submission API routes."""
import io
import json
import os
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File
import httpx
from anthropic import Anthropic

from app.database import get_db
from app.models import ReviewContext, ReviewSubmit, ReviewResponse
from app.services.summarisation import regenerate_summary_for_cycle

router = APIRouter()

# Extraction prompt for structuring voice transcripts
EXTRACTION_PROMPT = """Extract structured 360-degree feedback from this voice transcript.

Transcript:
"{transcript}"

Extract these fields. If a category isn't mentioned, return empty string.
Return valid JSON only, no explanation.

{{
  "start_doing": "What the employee should begin doing",
  "stop_doing": "What the employee should stop doing",
  "continue_doing": "What the employee should keep doing",
  "example": "A specific example or story mentioned",
  "additional": "Any other relevant comments"
}}"""


@router.get("/review/{token}", response_model=ReviewContext)
def get_review_context(token: str, db=Depends(get_db)):
    """Get context for a review form (employee name, relationship)."""
    cur = db.cursor()

    cur.execute(
        """SELECT r.name as reviewer_name, r.relationship, r.id as reviewer_id,
                  u.name as employee_name
           FROM reviewers r
           JOIN feedback_cycles fc ON r.cycle_id = fc.id
           JOIN users u ON fc.subject_user_id = u.id
           WHERE r.token = %s""",
        (token,)
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Invalid review link")

    # Check if already submitted
    cur.execute(
        "SELECT id FROM reviews WHERE reviewer_id = %s",
        (row["reviewer_id"],)
    )
    submitted = cur.fetchone()

    return ReviewContext(
        employee_name=row["employee_name"],
        relationship=row["relationship"],
        reviewer_name=row["reviewer_name"],
        already_submitted=submitted is not None
    )


@router.post("/review/{token}", response_model=ReviewResponse)
def submit_review(
    token: str,
    review: ReviewSubmit,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    """Submit feedback for a review."""
    cur = db.cursor()

    # Get reviewer info including cycle_id for background task
    cur.execute(
        "SELECT id, cycle_id FROM reviewers WHERE token = %s",
        (token,)
    )
    reviewer = cur.fetchone()

    if not reviewer:
        raise HTTPException(status_code=404, detail="Invalid review link")

    # Check if already submitted
    cur.execute(
        "SELECT id FROM reviews WHERE reviewer_id = %s",
        (reviewer["id"],)
    )
    existing = cur.fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted")

    # Insert review
    cur.execute(
        """INSERT INTO reviews (reviewer_id, start_doing, stop_doing, continue_doing, example, additional)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
        (reviewer["id"], review.start_doing, review.stop_doing, review.continue_doing, review.example, review.additional)
    )
    row = cur.fetchone()
    db.commit()

    # Trigger summary regeneration in background
    background_tasks.add_task(regenerate_summary_for_cycle, reviewer["cycle_id"])

    return ReviewResponse(
        id=row["id"],
        reviewer_id=row["reviewer_id"],
        start_doing=row["start_doing"],
        stop_doing=row["stop_doing"],
        continue_doing=row["continue_doing"],
        example=row["example"],
        additional=row["additional"],
        submitted_at=row["submitted_at"]
    )


@router.post("/review/{token}/voice-transcribe")
async def transcribe_voice_feedback(
    token: str,
    audio_file: UploadFile = File(...),
    db=Depends(get_db)
):
    """Transcribe and structure voice feedback using Whisper and Claude."""
    cur = db.cursor()

    # Validate token exists and review not already submitted
    cur.execute(
        "SELECT id, cycle_id FROM reviewers WHERE token = %s",
        (token,)
    )
    reviewer = cur.fetchone()

    if not reviewer:
        raise HTTPException(status_code=404, detail="Invalid review link")

    # Check if already submitted
    cur.execute(
        "SELECT id FROM reviews WHERE reviewer_id = %s",
        (reviewer["id"],)
    )
    existing = cur.fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="Feedback already submitted")

    # Read and validate file size
    contents = await audio_file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="File too large")

    # Prepare audio buffer
    audio_buffer = io.BytesIO(contents)
    audio_buffer.name = audio_file.filename or "recording.webm"

    # Transcribe with Whisper API (direct HTTP call - Vercel compatible)
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                'https://api.openai.com/v1/audio/transcriptions',
                headers={'Authorization': f'Bearer {openai_api_key}'},
                files={'file': (audio_buffer.name, audio_buffer, 'audio/webm')},
                data={'model': 'whisper-1', 'response_format': 'text'}
            )
            response.raise_for_status()
            transcript = response.text.strip()

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 401:
            raise HTTPException(status_code=500, detail="API authentication failed")
        elif status == 413:
            raise HTTPException(status_code=400, detail="Audio file too large")
        elif status == 400:
            raise HTTPException(status_code=400, detail="Invalid audio format")
        elif status == 429:
            raise HTTPException(status_code=429, detail="Rate limited, please try again")
        else:
            raise HTTPException(status_code=503, detail="Transcription service unavailable")

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Transcription timed out")

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

    # Validate transcript
    if not transcript or len(transcript) < 10:
        raise HTTPException(
            status_code=400,
            detail="No speech detected. Please speak clearly and try again."
        )

    # Structure with Claude Haiku
    anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    try:
        structured = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(transcript=transcript)}]
        )

        fields = json.loads(structured.content[0].text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

    return fields
