#!/usr/bin/env python3
"""Reset demo data to allow re-submission of reviews."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from app.database import get_connection


def reset_demo_data():
    """
    Reset demo accounts by:
    1. Deleting all reviews for demo reviewers
    2. Deleting all summaries for demo cycles
    3. Keeping users, cycles, and reviewers (tokens still work)
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get all demo user IDs
    cur.execute("SELECT id FROM users WHERE is_demo = TRUE")
    demo_user_ids = [row["id"] for row in cur.fetchall()]

    if not demo_user_ids:
        print("No demo users found. Nothing to reset.")
        cur.close()
        conn.close()
        return

    print(f"Found {len(demo_user_ids)} demo users")

    # Get all feedback cycles for demo users
    cur.execute(
        "SELECT id FROM feedback_cycles WHERE subject_user_id = ANY(%s)",
        (demo_user_ids,)
    )
    demo_cycle_ids = [row["id"] for row in cur.fetchall()]
    print(f"Found {len(demo_cycle_ids)} demo cycles")

    # Get all reviewers for demo cycles
    cur.execute(
        "SELECT id FROM reviewers WHERE cycle_id = ANY(%s)",
        (demo_cycle_ids,)
    )
    demo_reviewer_ids = [row["id"] for row in cur.fetchall()]
    print(f"Found {len(demo_reviewer_ids)} demo reviewers")

    # Count existing reviews
    cur.execute(
        "SELECT COUNT(*) as count FROM reviews WHERE reviewer_id = ANY(%s)",
        (demo_reviewer_ids,)
    )
    review_count = cur.fetchone()["count"]
    print(f"Found {review_count} existing reviews")

    # Count existing summaries
    cur.execute(
        "SELECT COUNT(*) as count FROM summaries WHERE cycle_id = ANY(%s)",
        (demo_cycle_ids,)
    )
    summary_count = cur.fetchone()["count"]
    print(f"Found {summary_count} existing summaries")

    # Delete reviews for demo reviewers
    if review_count > 0:
        cur.execute(
            "DELETE FROM reviews WHERE reviewer_id = ANY(%s)",
            (demo_reviewer_ids,)
        )
        print(f"✓ Deleted {review_count} reviews")

    # Delete summaries for demo cycles
    if summary_count > 0:
        cur.execute(
            "DELETE FROM summaries WHERE cycle_id = ANY(%s)",
            (demo_cycle_ids,)
        )
        print(f"✓ Deleted {summary_count} summaries")

    # Fix manager_user_id on demo cycles if not set
    # (ensures Sam Taylor is set as manager for Alex Chen's cycle)
    cur.execute("""
        UPDATE feedback_cycles fc
        SET manager_user_id = (SELECT id FROM users WHERE email = 'sam@demo.360feedback')
        WHERE fc.subject_user_id IN (SELECT id FROM users WHERE email = 'alex@demo.360feedback')
        AND fc.manager_user_id IS NULL
    """)
    if cur.rowcount > 0:
        print(f"✓ Fixed manager_user_id on {cur.rowcount} cycle(s)")

    # Commit changes
    conn.commit()
    cur.close()
    conn.close()

    print("\n✅ Demo data reset complete!")
    print("\nDemo tokens ready for use:")
    print("  - Sam Taylor (Manager, Weekly):     demo-sam-token-abc123")
    print("  - Jordan Lee (Peer, Weekly):        demo-jordan-token-def456")
    print("  - Casey Morgan (Direct Report, Monthly): demo-casey-token-ghi789")
    print("  - Riley Kumar (Cross-functional, Rarely): demo-riley-token-jkl012")
    print("\nReview form: /review/{token}")
    print("Manager dashboard: /manager/1")


if __name__ == "__main__":
    try:
        reset_demo_data()
    except Exception as e:
        print(f"❌ Error resetting demo data: {e}")
        sys.exit(1)
