"""AI summarisation service using Claude API."""
import logging
import os
from anthropic import Anthropic

logger = logging.getLogger(__name__)

# Weighting factors
RELATIONSHIP_WEIGHTS = {
    "manager": 1.0,
    "peer": 0.8,
    "direct_report": 0.7,
    "xfn": 0.6,
}

FREQUENCY_WEIGHTS = {
    "weekly": 1.0,
    "monthly": 0.7,
    "rarely": 0.4,
}

RELATIONSHIP_LABELS = {
    "manager": "Manager",
    "peer": "Peer",
    "direct_report": "Direct Report",
    "xfn": "Cross-functional",
}

FREQUENCY_LABELS = {
    "weekly": "weekly",
    "monthly": "monthly",
    "rarely": "rarely",
}


def calculate_weight(relationship: str, frequency: str) -> float:
    """Calculate combined weight from relationship and frequency."""
    rel_weight = RELATIONSHIP_WEIGHTS.get(relationship, 0.5)
    freq_weight = FREQUENCY_WEIGHTS.get(frequency, 0.5)
    return round(rel_weight * freq_weight, 2)


def generate_summary(employee_name: str, reviews: list[dict]) -> tuple[str, str]:
    """
    Generate AI summary from reviews.

    Args:
        employee_name: Name of the employee being reviewed
        reviews: List of review dicts with reviewer info

    Returns:
        Tuple of (summary_content, weighting_explanation)
    """
    # Build feedback section for prompt
    feedback_sections = []
    weighted_reviews = []

    for review in reviews:
        weight = calculate_weight(review["relationship"], review["frequency"])
        rel_label = RELATIONSHIP_LABELS.get(review["relationship"], review["relationship"])
        freq_label = FREQUENCY_LABELS.get(review["frequency"], review["frequency"])

        weighted_reviews.append({
            "name": review["reviewer_name"],
            "relationship": rel_label,
            "frequency": freq_label,
            "weight": weight,
        })

        section = f"""### Reviewer: {review["reviewer_name"]} ({rel_label}, works together {freq_label})
**Weight**: {weight} (based on relationship and collaboration frequency)

**Start doing**: {review["start_doing"]}

**Stop doing**: {review["stop_doing"]}

**Continue doing**: {review["continue_doing"]}

**Example**: {review["example"]}

**Additional**: {review["additional"] or "N/A"}
"""
        feedback_sections.append(section)

    feedback_text = "\n---\n".join(feedback_sections)

    prompt = f"""You are summarising 360-degree feedback for an employee performance review.

## Employee
{employee_name}

## Feedback Submissions

{feedback_text}

## Instructions
Synthesise this feedback into a summary with these sections:
1. **Strengths** - What this person does well (weight higher-confidence feedback more heavily)
2. **Growth Areas** - Where they can improve
3. **Key Examples** - Specific behaviours observed (quote or paraphrase from feedback)
4. **Suggested Focus** - 1-2 priority areas for development

Weight feedback from managers and frequent collaborators more heavily than occasional cross-functional contacts.

Keep the tone constructive and actionable. Be concise. Use markdown formatting.
"""

    # Call Claude API
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    summary_content = message.content[0].text

    # Generate weighting explanation
    highest_weight_reviewer = max(weighted_reviews, key=lambda x: x["weight"])
    weighting_explanation = (
        f"This summary weights feedback based on reviewer relationship "
        f"(manager feedback weighted highest) and collaboration frequency "
        f"(weekly interactions weighted highest). {highest_weight_reviewer['name']}'s "
        f"feedback as a {highest_weight_reviewer['relationship'].lower()} with "
        f"{highest_weight_reviewer['frequency']} interaction carried the most weight."
    )

    return summary_content, weighting_explanation


def regenerate_summary_for_cycle(cycle_id: int):
    """
    Background task to regenerate summary after review submission.

    Conditions:
    - At least 2 reviews must exist
    - Summary must NOT be finalised
    """
    from app.database import get_connection
    from datetime import datetime

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Check review count
        cur.execute(
            """SELECT COUNT(*) as count FROM reviews r
               JOIN reviewers rv ON r.reviewer_id = rv.id
               WHERE rv.cycle_id = %s""",
            (cycle_id,)
        )
        review_count = cur.fetchone()["count"]

        if review_count < 2:
            logger.info(f"Cycle {cycle_id}: Only {review_count} reviews, skipping regeneration")
            return

        # Check if summary exists and is finalised
        cur.execute(
            "SELECT id, finalised FROM summaries WHERE cycle_id = %s",
            (cycle_id,)
        )
        existing_summary = cur.fetchone()

        if existing_summary and existing_summary["finalised"]:
            logger.info(f"Cycle {cycle_id}: Summary is finalised, skipping regeneration")
            return

        # Get subject name for generation
        cur.execute(
            """SELECT u.name as subject_name
               FROM feedback_cycles fc
               JOIN users u ON fc.subject_user_id = u.id
               WHERE fc.id = %s""",
            (cycle_id,)
        )
        cycle_info = cur.fetchone()
        subject_name = cycle_info["subject_name"]

        # Fetch reviews with weighting info
        cur.execute(
            """SELECT rev.*, r.name as reviewer_name, r.relationship, r.frequency
               FROM reviews rev
               JOIN reviewers r ON rev.reviewer_id = r.id
               WHERE r.cycle_id = %s""",
            (cycle_id,)
        )
        reviews = [dict(row) for row in cur.fetchall()]

        # Generate summary
        summary_content, weighting_explanation = generate_summary(subject_name, reviews)

        # Save or update summary
        now = datetime.now()
        if existing_summary:
            cur.execute(
                """UPDATE summaries
                   SET content = %s, weighting_explanation = %s, updated_at = %s
                   WHERE cycle_id = %s""",
                (summary_content, weighting_explanation, now, cycle_id)
            )
        else:
            cur.execute(
                """INSERT INTO summaries (cycle_id, content, weighting_explanation, updated_at)
                   VALUES (%s, %s, %s, %s)""",
                (cycle_id, summary_content, weighting_explanation, now)
            )

        conn.commit()
        logger.info(f"Cycle {cycle_id}: Summary regenerated successfully")

    except Exception as e:
        logger.exception(f"Cycle {cycle_id}: Failed to regenerate summary: {e}")
        # Don't re-raise - background task failures should be silent
    finally:
        if conn:
            conn.close()
