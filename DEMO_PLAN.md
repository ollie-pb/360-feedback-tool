# 360 Feedback Tool - Demo Plan

Structured demo walkthroughs for showcasing the tool to different audiences.

## Demo Scenarios

| Scenario | Duration | Audience | Focus |
|----------|----------|----------|-------|
| **Quick Demo** | 5 min | Executives, first impressions | Voice + AI summary "wow factor" |
| **Full Walkthrough** | 15 min | Product teams, clients | Complete feedback cycle |
| **Deep Dive** | 25 min | Technical teams | Architecture & implementation |

---

## Scenario 1: Quick Demo (5 min)

**Key Message**: "360 feedback that used to take hours now takes minutes."

### Setup
- Open reviewer form: `/review/demo-riley-token-jkl012`
- Open manager dashboard: `/manager/1`
- Test microphone permissions

### Flow

**1. Voice Recording (2 min)**
- Navigate to review form
- Click microphone on "Start Doing" field
- Speak: "Alex should start delegating more code reviews to senior engineers. This would free up time for strategic planning."
- Stop recording, show processing
- **Highlight**: Field auto-populates with structured, professional text

**2. AI Summary (2 min)**
- Navigate to manager dashboard (`/manager/1`)
- Show progress: "3 of 4 reviews submitted"
- Scroll to AI summary with structured sections
- **Highlight**: Weighted synthesis (Manager 1.0x, Peer 0.8x, etc.)

**3. Edit & Finalize (1 min)**
- Click "Edit Summary", make a small change
- Show "Finalize Summary" button
- **Closing**: "AI does 90% of the work, managers keep control."

---

## Scenario 2: Full Walkthrough (15 min)

**Key Message**: "End-to-end feedback cycle with AI at every step."

### Setup
- Open dashboard: `/dashboard`
- Have 2-3 browser tabs ready
- Prepare voice feedback example

### Flow

**1. Create Feedback Cycle (3 min)**
- Create new cycle for "Alex Chen"
- Add reviewers with weighting:
  - Riley Martinez (Manager, Weekly) → 1.0x weight
  - Jordan Park (Peer, Weekly) → 0.8x weight
  - Sam Kim (Direct Report, Monthly) → 0.49x weight
- Show unique review links generated
- **Highlight**: Weighting = relationship × frequency

**2. Submit Feedback with Voice (5 min)**
- Open reviewer link
- Record "Start Doing" field via voice
- Record "Continue Doing" field via voice
- Type "Stop Doing" field (show flexibility)
- Submit feedback
- **Highlight**: Per-field recording (not one long recording)

**3. Review AI Summary (4 min)**
- Navigate to manager dashboard
- Show cycle overview and reviewer status table
- Scroll to AI-generated summary with structure:
  - Key Strengths
  - Areas for Growth
  - Specific Examples
- Edit summary, save changes
- Finalize cycle
- **Highlight**: Automatic generation + human editing

**4. Reviewer Inbox (2 min)**
- Navigate to inbox (`/inbox/jordan@company.com`)
- Show pending and completed reviews
- **Highlight**: Centralized reviewer experience

**Q&A (1 min)**
- Customizable fields? → Roadmap item
- AI model? → Claude Sonnet 4.5 + Haiku
- Transcription time? → 5-10 seconds per minute of audio

---

## Scenario 3: Deep Dive (25 min)

**Key Message**: "Modern architecture with AI intelligence at scale."

### Setup
- Have API docs open (`/docs`)
- Terminal ready
- Browser DevTools open

### Flow

**1. Architecture (5 min)**
- Show tech stack:
  ```
  Frontend (Vanilla JS) → FastAPI → PostgreSQL
                       ↓
                  AI Services (Claude + Whisper)
  ```
- Navigate to `/docs`, show auto-generated API
- Explain serverless deployment on Vercel
- **Highlight**: Zero infrastructure, auto-scaling

**2. Voice Recording Deep Dive (8 min)**
- Open DevTools Network tab
- Record audio, show:
  - MediaRecorder API usage
  - POST to `/api/review/{token}/voice-transcribe`
  - Multipart form: `audio_file` + `field_name`
- Show backend code (`app/routes/review.py`):
  - Stage 1: Whisper transcription (~$0.006/min)
  - Stage 2: Claude Haiku extraction (~$0.001)
- Show field-specific extraction prompts with examples
- **Highlight**: Two-stage AI processing for accuracy + structure

**3. Weighting Algorithm (5 min)**
- Show database query calculating weights
- Show weighted context in summarization prompt:
  ```
  [Weight: 1.00] Riley (Manager, Weekly): ...
  [Weight: 0.80] Jordan (Peer, Weekly): ...
  [Weight: 0.49] Sam (Direct Report, Monthly): ...
  ```
- Explain: Mathematical weighting, not just prompt engineering
- **Highlight**: Transparent, prevents gaming

**4. Summarization Engine (4 min)**
- Show code (`app/services/summarisation.py`):
  - Fetch reviews
  - Calculate weights
  - Build weighted context
  - Call Claude Sonnet (temp 0.3, 2048 tokens)
  - Store summary
- Show background task processing (async)
- **Highlight**: Auto-regenerates on each new review

**5. Deployment (3 min)**
- Show `vercel.json` configuration
- Explain serverless functions (one per route)
- Environment variables (API keys, DATABASE_URL)
- Connection pooling for database
- **Highlight**: Deploy with `vercel --prod`

---

## Demo Tips

### Pre-Demo Checklist
- [ ] Test demo environment running
- [ ] Verify API keys valid
- [ ] Test microphone permissions
- [ ] Open all URLs in tabs
- [ ] Turn off notifications
- [ ] Set browser zoom to 125%

### Common Issues & Recovery

| Issue | Recovery |
|-------|----------|
| Voice recording fails | Show typed input: "Voice works the same way" |
| AI processing slow | "While this processes, let me show the summary..." |
| Database error | Show pre-captured screenshots/video |
| Can't answer question | "Great question - let me follow up offline" |

### Audience Adjustments

- **Executives**: Focus on ROI, time savings ("5 hours saved per cycle")
- **HR Teams**: Focus on workflow, compliance, privacy considerations
- **Engineering**: Show API docs, architecture decisions, scalability
- **Product Teams**: Focus on UX, design decisions, roadmap

---

## Key Talking Points

### Voice Recording
> "Instead of typing 5-10 minutes of feedback, reviewers speak naturally for 30 seconds per field. The AI transcribes and structures it professionally."

### AI Summary
> "We have reviews from a manager, peer, and direct report. Our AI synthesizes these with appropriate weighting—manager feedback carries full weight, while infrequent collaborators have less influence."

### Complete Cycle
> "What used to take HR teams 2-3 hours of manual synthesis now happens automatically in minutes, while managers retain full editing control."

---

## Demo Data Reference

**Cycle 1: Alex Chen (Senior Engineer)**
- Status: In Progress (3 of 4 reviews submitted)

**Reviewers:**
1. ✅ Riley Martinez (Manager, Weekly, 1.0x) - `demo-riley-token-abc123`
2. ✅ Jordan Park (Peer, Weekly, 0.8x) - `demo-jordan-token-def456`
3. ✅ Sam Kim (Direct Report, Monthly, 0.49x) - `demo-sam-token-ghi789`
4. ⏳ Taylor Brooks (Cross-functional, Rarely, 0.24x) - `demo-taylor-token-jkl012` ← Use for live demo

**URLs:**
- Manager Dashboard: `/manager/1`
- Reviewer Inbox: `/inbox/jordan@company.com`

---

## Frequently Asked Questions

**Q: How accurate is voice transcription?**
A: Whisper achieves 95%+ accuracy. Reviewers can edit before submitting.

**Q: Can we customize feedback fields?**
A: Currently fixed to start/stop/continue. Custom fields on roadmap.

**Q: What's the cost per cycle?**
A: ~$0.05-0.10 per cycle (voice + summary generation).

**Q: GDPR compliance?**
A: Tool doesn't store recordings. Implement data retention policies for production.

**Q: Integration with HRIS?**
A: Full REST API available for integration.

---

**Last Updated**: 2026-01-23
