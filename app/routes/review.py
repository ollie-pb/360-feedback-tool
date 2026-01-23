"""Review submission API routes."""
import io
import json
import os
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, File, Form

from app.database import get_db
from app.models import ReviewContext, ReviewSubmit, ReviewResponse
from app.services.summarisation import regenerate_summary_for_cycle

router = APIRouter()

# Temperature recommendation: 0.3-0.4
# This gives enough variability for natural language while maintaining consistency
EXTRACTION_TEMPERATURE = 0.35

FIELD_EXTRACTION_PROMPTS = {
    "start_doing": """Transform this voice feedback into a constructive "Start Doing" recommendation.

Example input: "I think she could really benefit from speaking up more in client meetings. She clearly has good ideas because I see them in her written work, but she tends to stay quiet when the clients are in the room. It would really help her visibility and I think the clients would appreciate hearing directly from her."

Example output: "Consider taking a more active voice in client meetings. Your ideas come through strongly in written deliverables, and sharing them directly during discussions would increase your visibility with clients and strengthen the team's presence. Starting with one or two prepared points per meeting could be a comfortable way to build this habit."

---

Transcript: "{transcript}"

Guidelines:
- Extract suggestions for NEW behaviors, skills, or approaches the person should begin
- Write 2-4 sentences that capture the full substance of what was said
- Frame recommendations around observable behaviors and actions, not personality traits
- Include the reasoning or potential impact if the speaker mentioned it
- Use professional, encouraging language (e.g., "Consider developing..." or "It would be valuable to...")
- Preserve specific details, contexts, or situations mentioned

If no "start doing" content is present, return an empty string.
Return plain text only.""",

    "stop_doing": """Transform this voice feedback into constructive "Stop Doing" feedback.

Example input: "Honestly he just talks over everyone in meetings, it's really frustrating. Like last week in the planning session he just wouldn't let anyone finish their point. And he does this thing where he'll ask for input and then immediately shut it down which makes people not want to contribute."

Example output: "Consider giving colleagues more space to complete their thoughts during discussions. In recent planning meetings, there have been moments where jumping in before others finish has made it harder for the team to fully share their perspectives. When soliciting input, allowing time for ideas to be fully explored before responding would encourage more open contribution from the team."

---

Transcript: "{transcript}"

Guidelines:
- Extract behaviors, habits, or approaches the person should discontinue or reduce
- Write 2-4 sentences that capture the full substance while remaining constructive
- Frame as behaviors to change, not character flaws (e.g., "Reduce the frequency of..." rather than "Stop being...")
- Include context about why this change would be beneficial if mentioned
- Preserve specific examples or situations referenced, as these add clarity
- Use professional language that focuses on impact rather than blame

If no "stop doing" content is present, return an empty string.
Return plain text only.""",

    "continue_doing": """Transform this voice feedback into "Continue Doing" recognition.

Example input: "She's honestly one of the best at keeping projects on track. Like whenever things start to slip she's the first one to flag it and she does it in a way that doesn't make people defensive. The weekly check-ins she runs are really well structured too, everyone always knows where things stand afterwards."

Example output: "Your proactive approach to project management is a real strength. You consistently identify potential delays early and raise them in a way that keeps the team focused rather than defensive. The weekly check-ins you facilitate are well-structured and leave everyone with clear visibility into project status—this is valuable and worth maintaining."

---

Transcript: "{transcript}"

Guidelines:
- Extract strengths, effective behaviors, and approaches worth maintaining
- Write 2-4 sentences that capture what's working and why it matters
- Be specific about the behaviors and their positive impact
- Include any context about when or how these strengths show up
- Use affirming language that reinforces the value of these behaviors
- Preserve details that make the feedback feel genuine and specific

If no "continue doing" content is present, return an empty string.
Return plain text only.""",

    "example": """Extract and refine a specific example or story from this feedback.

Example input: "There was this one time during the product launch last quarter where everything was going wrong, the vendor was late, marketing had the wrong assets, and instead of panicking he just calmly worked through each issue one by one. He got on the phone with the vendor, found a workaround for the assets thing, and we actually launched on time. It was impressive."

Example output: "During last quarter's product launch, multiple issues emerged simultaneously—the vendor was delayed and marketing had received incorrect assets. Rather than escalating the stress, he methodically addressed each problem: coordinating directly with the vendor to resolve the delay and identifying a workaround for the asset issue. The launch proceeded on schedule, demonstrating strong composure and problem-solving under pressure."

---

Transcript: "{transcript}"

Guidelines:
- Identify concrete situations, observations, or stories that illustrate the feedback
- Write 3-5 sentences preserving the narrative arc: situation, behavior observed, and outcome/impact
- Keep specific details (projects, meetings, timeframes) that add credibility
- Frame objectively, describing what happened rather than judging character
- If multiple examples exist, capture the most illustrative one in full detail
- The example should feel like a real moment, not a generic observation

If no specific example is present, return an empty string.
Return plain text only.""",

    "additional": """Extract additional context or observations from this feedback.

Example input: "Just want to add that I know he's been dealing with a lot since taking over the new team, so some of this might just be adjustment. I think with some coaching on the communication stuff he could be really effective. Maybe pairing him with Sarah who's great at this could help."

Example output: "It's worth noting that much of this feedback comes during a transition period after taking on a new team, which may be contributing to some of the challenges observed. With targeted support around communication approaches, there's strong potential for growth. Mentorship or collaboration with colleagues who excel in this area could accelerate development."

---

Transcript: "{transcript}"

Guidelines:
- Capture important nuances, caveats, or context not covered in start/stop/continue
- Include any overall impressions, relationship context, or environmental factors mentioned
- Write 2-4 sentences if substantial additional content exists
- Preserve the speaker's intent while maintaining professional framing
- Include any suggestions for resources, support, or development opportunities mentioned

If no additional content is present, return an empty string.
Return plain text only."""
}

# Keep original prompt for backwards compatibility
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
    field_name: str = Form(None),
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
    import httpx

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
    from anthropic import Anthropic
    anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    try:
        if field_name:
            # Per-field extraction
            if field_name not in FIELD_EXTRACTION_PROMPTS:
                raise HTTPException(status_code=400, detail=f"Invalid field name: {field_name}")

            prompt = FIELD_EXTRACTION_PROMPTS[field_name].format(transcript=transcript)
            structured = anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,  # Increased for detailed 2-5 sentence responses
                temperature=EXTRACTION_TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            field_value = structured.content[0].text.strip()
            return {"field_value": field_value}
        else:
            # Legacy: Extract all fields (backwards compatible)
            structured = anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                temperature=EXTRACTION_TEMPERATURE,
                messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(transcript=transcript)}]
            )
            fields = json.loads(structured.content[0].text)
            return fields

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")
