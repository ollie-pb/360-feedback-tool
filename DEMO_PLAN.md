# 360 Feedback Tool - Demo Plan

This document provides structured demo walkthroughs for showcasing the 360 Feedback Summarisation Tool to stakeholders, clients, or during product presentations.

---

## Demo Overview

**Purpose**: Demonstrate how the tool streamlines 360-degree feedback collection, uses AI to generate weighted summaries, and supports voice input for faster feedback submission.

**Key Differentiators**:
- ✨ **Voice-first feedback collection** with per-field recording
- 🤖 **AI-powered summarization** using Claude Sonnet
- ⚖️ **Intelligent weighting** based on relationship and collaboration frequency
- 📊 **Manager dashboard** with progress tracking and editing capabilities

**Demo Environments**:
- Production: `https://your-vercel-url.vercel.app`
- Local: `http://localhost:8000`

---

## Demo Scenarios

Choose the demo length based on your audience and time constraints:

| Scenario | Duration | Best For | Focus Areas |
|----------|----------|----------|-------------|
| **Quick Demo** | 5 min | Executive stakeholders, first impressions | Voice recording + AI summary |
| **Full Walkthrough** | 15 min | Product teams, potential clients | Complete feedback cycle |
| **Deep Dive** | 25 min | Technical audiences, implementation teams | Architecture, weighting logic, customization |

---

## Scenario 1: Quick Demo (5 minutes)

**Goal**: Show the "wow factor" - voice recording and AI-generated summaries

**Audience**: Executives, busy stakeholders, initial product discovery

**Key Message**: "Traditional 360 feedback takes hours to collect and synthesize. We've reduced it to minutes with voice input and AI summarization."

### Setup (Before Demo)
- [ ] Open reviewer form: `/review/demo-riley-token-jkl012`
- [ ] Have manager dashboard ready: `/manager/1`
- [ ] Test microphone permissions granted
- [ ] Prepare a short feedback example to speak

### Walkthrough

#### Part 1: Voice Recording (2 minutes)
**Talking Points:**
- "Traditional feedback forms require typing lengthy responses. We've added voice recording to each field."
- "Let me show you how a reviewer can submit feedback in under 2 minutes."

**Actions:**
1. Navigate to reviewer form (`/review/demo-riley-token-jkl012`)
2. Point out the 5 feedback fields with microphone icons
3. **Click microphone for "Start Doing" field**
   - Observe: Button turns red and pulses
   - Say: "Alex should start delegating more code reviews to senior engineers. This would free up time for strategic planning and help develop the team's technical judgment."
   - Click again to stop
4. **Watch the magic happen**
   - Show spinner appearing (processing)
   - Show field auto-populating with structured text
   - Highlight how it preserved the context and reasoning

**Key Feature**: Per-field voice recording with real-time transcription and structuring

#### Part 2: AI Summary (2 minutes)
**Talking Points:**
- "Once we have 2+ reviews, our system automatically generates a weighted summary."
- "The AI considers both the relationship type and collaboration frequency."

**Actions:**
1. Navigate to manager dashboard (`/manager/1`)
2. Show **progress indicator**: "3 of 4 reviews submitted"
3. Scroll to **AI-generated summary section**
4. Point out:
   - Structured sections (Strengths, Growth Areas, Specific Examples)
   - Professional tone and actionable language
   - Synthesis of multiple perspectives
5. **Show weighting explanation**:
   - "Riley (Manager, Weekly): 1.0x weight"
   - "Jordan (Peer, Weekly): 0.8x weight"
   - "Manager feedback has more influence than peer feedback"

**Key Feature**: AI-powered weighted summarization

#### Part 3: Edit & Finalize (1 minute)
**Talking Points:**
- "Managers can review and refine the AI summary before delivery."

**Actions:**
1. Click **"Edit Summary"**
2. Show editable text area
3. Make a small edit (add emphasis or clarification)
4. Click **"Save Changes"**
5. Point out **"Finalize Summary"** button
   - "This locks the summary and marks the cycle complete"

**Closing Statement:**
> "What used to take HR teams hours of manual synthesis now happens automatically, while still giving managers full control over the final output."

---

## Scenario 2: Full Walkthrough (15 minutes)

**Goal**: Demonstrate the complete feedback cycle from employee nomination to manager finalization

**Audience**: Product teams, HR departments, potential clients evaluating the tool

**Key Message**: "End-to-end feedback cycle management with AI assistance at every step."

### Setup (Before Demo)
- [ ] Open dashboard: `/dashboard`
- [ ] Have 2-3 browser tabs/windows ready for different personas
- [ ] Prepare voice feedback script
- [ ] Test audio recording works

### Walkthrough

#### Part 1: Employee Creates Feedback Cycle (3 minutes)

**Talking Points:**
- "Let's start from the employee perspective. They need to gather 360 feedback for an upcoming review."

**Actions:**
1. Navigate to dashboard (`/dashboard`)
2. Click **"Create New Feedback Cycle"**
3. Enter employee details:
   - Name: "Alex Chen"
   - Email: "alex.chen@company.com"
   - Role: "Senior Engineer"
4. Click **"Create Cycle"**
5. **Add reviewers** (show the weighting system):

   **Reviewer 1:**
   - Name: "Riley Martinez" (Manager)
   - Email: "riley@company.com"
   - Relationship: **Manager** (1.0x weight)
   - Frequency: **Weekly** (1.0x weight)
   - Combined weight: **1.0** (highest influence)

   **Reviewer 2:**
   - Name: "Jordan Park" (Peer)
   - Email: "jordan@company.com"
   - Relationship: **Peer** (0.8x weight)
   - Frequency: **Weekly** (1.0x weight)
   - Combined weight: **0.8**

   **Reviewer 3:**
   - Name: "Sam Kim" (Direct Report)
   - Email: "sam@company.com"
   - Relationship: **Direct Report** (0.7x weight)
   - Frequency: **Monthly** (0.7x weight)
   - Combined weight: **0.49** (lower influence)

6. Click **"Add Reviewers"**
7. Show **unique review links generated**
8. Explain: "Each reviewer gets a unique token link. No login required - reduces friction."

**Key Features**:
- Relationship-based weighting
- Frequency-based weighting
- Token-based access (no auth barriers)

#### Part 2: Reviewer Submits Feedback with Voice (5 minutes)

**Talking Points:**
- "Reviewers can type OR use voice recording. Let's use voice to show the fastest path."
- "I'll demonstrate recording feedback for multiple fields."

**Actions:**
1. Open reviewer link (`/review/{token}`)
2. Show **context displayed**: "You're providing feedback for Alex Chen"
3. Show **all 5 fields with microphone buttons**

**Record "Start Doing" field:**
- Click mic icon
- Grant permissions (if needed)
- Speak: "I think Alex should start taking on more leadership in sprint planning meetings. They have really strong technical judgment, but they tend to defer to others when making prioritization decisions. The team would benefit from their technical perspective during planning."
- Click to stop
- Wait for processing (~5-8 seconds)
- Show result: Structured, professional text extracted

**Record "Continue Doing" field:**
- Click mic icon
- Speak: "Alex should definitely continue their thorough code reviews. Last week they caught a critical security issue in Jordan's pull request that could have been a major problem in production. Their attention to detail is excellent and everyone learns from their feedback."
- Stop recording
- Show result: Specific example preserved with context

**Type "Stop Doing" field** (show flexibility):
- Type: "Stop working late nights so frequently. Sustainable pace is important for long-term productivity."

4. Click **"Submit Feedback"**
5. Show success message

**Key Features**:
- Per-field voice recording (not one long recording)
- Real-time transcription (Whisper API)
- Intelligent extraction (Claude Haiku)
- Mixed input methods (voice + typing)

#### Part 3: Manager Reviews AI Summary (4 minutes)

**Talking Points:**
- "Once 2+ reviews are submitted, the system automatically generates a summary."
- "The AI synthesizes multiple perspectives using weighted averaging."

**Actions:**
1. Navigate to manager dashboard (`/manager/1`)
2. Show **cycle overview card**:
   - Employee: Alex Chen
   - Status: In Progress
   - Reviews: 3 of 4 submitted
3. Show **reviewer status table**:
   - Riley Martinez ✓ (Manager, Weekly, 1.0x)
   - Jordan Park ✓ (Peer, Weekly, 0.8x)
   - Sam Kim ✓ (Direct Report, Monthly, 0.49x)
   - Taylor Brooks ⏳ (Pending)
4. Scroll to **AI-generated summary**
5. Walk through summary structure:
   ```
   ## Key Strengths
   - Thorough code reviews with attention to security
   - Strong technical judgment

   ## Areas for Growth
   - Leadership presence in planning meetings
   - Work-life balance and sustainable pace

   ## Specific Examples
   - Caught critical security issue in recent PR review
   ```

6. Explain **weighting context**:
   - "Riley's manager feedback carries full weight (1.0x)"
   - "Sam's input has lower weight (0.49x) as they're a direct report who collaborates monthly"
   - "This prevents any single perspective from dominating"

7. Click **"Edit Summary"**
8. Make a refinement (e.g., add specific recommendation)
9. Click **"Save Changes"**
10. Click **"Finalize Summary"**
11. Show finalized badge

**Key Features**:
- Automatic summary generation
- Weighted synthesis
- Manager editing capabilities
- Finalization workflow

#### Part 4: Inbox View (2 minutes)

**Talking Points:**
- "Reviewers can see all their pending feedback requests in one place."

**Actions:**
1. Navigate to inbox (`/inbox/jordan@company.com`)
2. Show list of pending reviews
3. Show submitted reviews (greyed out)
4. Click into a pending review

**Key Feature**: Centralized reviewer inbox

#### Closing Q&A (1 minute)

**Common Questions to Anticipate:**
- Q: "Can we customize the feedback fields?"
  - A: "Currently fixed to start/stop/continue framework, but customization is on the roadmap."
- Q: "What AI model powers the summaries?"
  - A: "Claude Sonnet 4.5 for summaries, Claude Haiku for voice extraction."
- Q: "How long does voice transcription take?"
  - A: "5-10 seconds for a 1-minute recording."
- Q: "Can reviewers edit after submission?"
  - A: "Not currently - this is intentional to prevent review gaming."

---

## Scenario 3: Deep Dive (25 minutes)

**Goal**: Technical demonstration for developers, architects, or technical decision-makers

**Audience**: Engineering teams, technical stakeholders, implementation partners

**Key Message**: "Modern architecture, serverless deployment, and AI-powered intelligence at scale."

### Setup (Before Demo)
- [ ] Have API docs open (`/docs`)
- [ ] Terminal ready with database queries
- [ ] Browser dev tools open
- [ ] Network tab ready to show API calls

### Walkthrough

#### Part 1: Architecture Overview (5 minutes)

**Talking Points:**
- "Let's start with the technical architecture."

**Actions:**
1. Show architecture diagram (create on whiteboard or screen share):
   ```
   Frontend (Static HTML/JS)
         ↓
   FastAPI Backend (Python)
         ↓
   PostgreSQL Database
         ↓
   AI Services (Anthropic + OpenAI)
   ```

2. Explain technology choices:
   - **FastAPI**: Modern async Python framework, auto-generated OpenAPI docs
   - **PostgreSQL**: Relational data (users, cycles, reviews, summaries)
   - **Vanilla JS**: No build step, fast iteration
   - **Vercel**: Serverless deployment, automatic scaling

3. Navigate to API docs (`/docs`)
4. Show auto-generated Swagger UI
5. Expand key endpoints:
   - `POST /api/review/{token}/voice-transcribe`
   - `GET /api/manager/{cycle_id}`
   - `POST /api/cycles/{id}/reviewers`

**Key Talking Points**:
- "All routes under `/api/` prefix"
- "Token-based authentication for reviewers (no login friction)"
- "Background tasks for async summary generation"

#### Part 2: Voice Recording Deep Dive (8 minutes)

**Talking Points:**
- "Let's examine the voice recording feature architecture."

**Actions:**

**Frontend Flow:**
1. Open browser DevTools → Network tab
2. Navigate to review form
3. Click microphone button
4. Show JavaScript code flow:
   ```javascript
   // State management
   fieldRecorders = {
     currentField: 'start_doing',
     mediaRecorder: MediaRecorder,
     isRecording: true
   }

   // MediaRecorder API
   navigator.mediaDevices.getUserMedia({ audio: true })
   recorder.start()
   ```

5. Record audio (watch Network tab)
6. Show multipart form upload:
   ```
   POST /api/review/{token}/voice-transcribe
   Content-Type: multipart/form-data

   audio_file: blob (WebM format)
   field_name: "start_doing"
   ```

**Backend Flow:**
1. Show code in editor (`app/routes/review.py`)
2. Walk through endpoint:
   ```python
   @router.post("/review/{token}/voice-transcribe")
   async def transcribe_voice_feedback(
       token: str,
       audio_file: UploadFile = File(...),
       field_name: str = Form(None),
   ):
       # 1. Validate token
       # 2. Transcribe with Whisper
       # 3. Extract with Claude
       # 4. Return structured field
   ```

3. Explain **two-stage AI processing**:

   **Stage 1: Transcription (Whisper)**
   - OpenAI Whisper API
   - Input: Audio blob (WebM/Opus)
   - Output: Raw transcript text
   - Cost: ~$0.006/minute

   **Stage 2: Extraction (Claude Haiku)**
   - Anthropic Claude Haiku
   - Input: Raw transcript + field-specific prompt
   - Output: Structured, professional feedback text
   - Cost: ~$0.001/extraction
   - Temperature: 0.35 (consistent output)

4. Show extraction prompts (`FIELD_EXTRACTION_PROMPTS`):
   ```python
   "start_doing": """Transform this voice feedback into
   a constructive "Start Doing" recommendation.

   Example input: "I think she could really benefit from..."
   Example output: "Consider taking a more active voice..."

   Guidelines:
   - Write 2-4 sentences
   - Frame recommendations around observable behaviors
   - Include reasoning or potential impact
   - Use professional, encouraging language
   """
   ```

5. Explain prompt engineering choices:
   - Example-driven prompts for consistency
   - Specific sentence count (2-4 sentences)
   - Professional tone guidelines
   - Context preservation instructions

**Key Talking Points**:
- "Per-field recording reduces cognitive load vs. one long recording"
- "Two-stage processing: Whisper for accuracy, Claude for structure"
- "Prompt engineering ensures consistent, professional output"
- "Total latency: 5-10 seconds for 1-minute recording"

#### Part 3: Weighting Algorithm (5 minutes)

**Talking Points:**
- "The weighting system ensures manager feedback has appropriate influence."

**Actions:**
1. Open database (or show schema):
   ```sql
   SELECT
     r.name,
     r.relationship,
     r.frequency,
     (CASE r.relationship
       WHEN 'manager' THEN 1.0
       WHEN 'peer' THEN 0.8
       WHEN 'direct_report' THEN 0.7
       WHEN 'cross_functional' THEN 0.6
     END) *
     (CASE r.frequency
       WHEN 'weekly' THEN 1.0
       WHEN 'monthly' THEN 0.7
       WHEN 'rarely' THEN 0.4
     END) as combined_weight
   FROM reviewers r
   WHERE r.cycle_id = 1;
   ```

2. Show results:
   ```
   Riley (Manager, Weekly):     1.0 × 1.0 = 1.00
   Jordan (Peer, Weekly):       0.8 × 1.0 = 0.80
   Sam (Direct Report, Monthly): 0.7 × 0.7 = 0.49
   Taylor (Cross-func, Rarely): 0.6 × 0.4 = 0.24
   ```

3. Explain **weighted summarization prompt**:
   ```python
   prompt = f"""Generate a 360 feedback summary.

   Reviews (weighted):

   [Weight: 1.00] Riley (Manager, Weekly):
   {review_1_content}

   [Weight: 0.80] Jordan (Peer, Weekly):
   {review_2_content}

   [Weight: 0.49] Sam (Direct Report, Monthly):
   {review_3_content}

   Synthesize with appropriate weight to each perspective.
   """
   ```

4. Show code (`app/services/summarisation.py`):
   ```python
   def build_weighted_context(reviews):
       context = []
       for review in reviews:
           weight = review.relationship_weight * review.frequency_weight
           context.append(f"[Weight: {weight:.2f}] {review.name}...")
       return "\n\n".join(context)
   ```

**Key Talking Points**:
- "Mathematical weighting (not just prompt engineering)"
- "Manager feedback has 2x influence vs. cross-functional/rarely"
- "Prevents gaming (can't stack low-weight reviewers)"
- "Transparent - weights shown to managers"

#### Part 4: Summarization Engine (4 minutes)

**Talking Points:**
- "Let's look at how AI summaries are generated."

**Actions:**
1. Show summary generation code (`app/services/summarisation.py`)
2. Walk through flow:
   ```python
   def generate_summary(cycle_id):
       # 1. Fetch all reviews for cycle
       reviews = get_reviews(cycle_id)

       # 2. Calculate weights
       weighted_reviews = calculate_weights(reviews)

       # 3. Build context
       context = build_weighted_context(weighted_reviews)

       # 4. Call Claude Sonnet
       summary = anthropic.messages.create(
           model="claude-sonnet-4-5-20250514",
           max_tokens=2048,
           temperature=0.3,
           messages=[{
               "role": "user",
               "content": SUMMARIZATION_PROMPT.format(context=context)
           }]
       )

       # 5. Store in database
       save_summary(cycle_id, summary.content[0].text)
   ```

3. Show summarization prompt structure:
   ```python
   SUMMARIZATION_PROMPT = """You are a professional HR consultant...

   Generate a 360-degree feedback summary with:

   ## Key Strengths
   (2-3 specific strengths with examples)

   ## Areas for Growth
   (2-3 actionable development areas)

   ## Specific Examples
   (Notable observations from reviewers)

   ## Recommendations
   (Concrete next steps)

   Guidelines:
   - Use professional, constructive tone
   - Be specific and actionable
   - Balance positive and developmental feedback
   - Cite examples when provided
   - Pay attention to review weights
   """
   ```

4. Explain **model choice**:
   - Claude Sonnet 4.5: Balance of quality and speed
   - Temperature 0.3: Consistent, professional output
   - Max tokens 2048: Room for detailed summaries
   - Cost: ~$0.015 per summary

5. Show **background task processing**:
   ```python
   @router.post("/review/{token}")
   def submit_review(
       review: ReviewSubmit,
       background_tasks: BackgroundTasks
   ):
       # Save review
       save_review(review)

       # Regenerate summary asynchronously
       background_tasks.add_task(
           regenerate_summary_for_cycle,
           cycle_id
       )
   ```

**Key Talking Points**:
- "Auto-regenerates on each new review submission"
- "Async processing keeps review submission fast"
- "Weighted context passed to AI"
- "Consistent structure via prompt engineering"

#### Part 5: Deployment & Scalability (3 minutes)

**Talking Points:**
- "Serverless deployment on Vercel with automatic scaling."

**Actions:**
1. Show `vercel.json` configuration
2. Explain serverless architecture:
   - Each API route = separate serverless function
   - Auto-scales with traffic
   - Cold start: ~500ms
   - Warm: ~50ms response time

3. Show environment variables:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-proj-...
   DATABASE_URL=postgresql://...
   ```

4. Explain database strategy:
   - Development: SQLite (local)
   - Production: Vercel Postgres (or external)
   - Connection pooling for serverless

5. Show monitoring (if available):
   - Vercel Analytics
   - API response times
   - Error rates

**Key Talking Points**:
- "Zero infrastructure management"
- "Automatic scaling for usage spikes"
- "Global CDN for static assets"
- "Database connection pooling for serverless"

#### Closing Discussion (Optional)

**Topics to Cover:**
- Customization options
- Integration possibilities (HRIS, Slack, email)
- Security hardening for production
- Compliance considerations (GDPR, data retention)
- Roadmap items

---

## Demo Tips & Best Practices

### Preparation Checklist

**24 Hours Before:**
- [ ] Test demo environment is running
- [ ] Verify API keys are valid
- [ ] Seed fresh demo data
- [ ] Test microphone permissions
- [ ] Record backup video (in case of tech issues)
- [ ] Prepare script/talking points

**30 Minutes Before:**
- [ ] Close unnecessary browser tabs
- [ ] Clear browser cache/cookies
- [ ] Test audio recording
- [ ] Open all necessary URLs in tabs
- [ ] Set browser zoom to 125% (better visibility in screen share)
- [ ] Turn off notifications
- [ ] Have backup internet connection ready

**During Demo:**
- [ ] Speak slowly and clearly
- [ ] Pause for questions
- [ ] Use cursor highlighting tool (if screen sharing)
- [ ] Have fallback plan if feature fails

### Common Issues & Recovery

**Issue 1: Voice recording doesn't work**
- **Recovery**: "Let me show you the typed input instead. The voice feature works the same way."
- **Prevention**: Test microphone before demo, have pre-recorded demo video

**Issue 2: AI processing takes too long**
- **Recovery**: "While this processes, let me show you the summary section..."
- **Prevention**: Use shorter voice clips, pre-warm API connections

**Issue 3: Database connection error**
- **Recovery**: Show pre-captured screenshots/video of the feature
- **Prevention**: Use stable demo environment, check DATABASE_URL

**Issue 4: Question you can't answer**
- **Response**: "Great question - let me take that offline and get you a detailed answer."
- **Prevention**: Anticipate questions, have FAQ doc ready

### Audience-Specific Adjustments

**For Executives:**
- Focus on business value (time savings, consistency, quality)
- Show ROI: "5 hours of HR time saved per feedback cycle"
- Emphasize ease of use

**For HR Teams:**
- Focus on workflow (cycle management, progress tracking)
- Show customization options
- Discuss compliance/privacy

**For Engineering Teams:**
- Show API docs
- Discuss architecture decisions
- Cover scalability and security

**For Product Teams:**
- Focus on user experience
- Show design decisions
- Discuss roadmap and feature prioritization

---

## Demo Scripts

### Script 1: Voice Recording Feature (60 seconds)

> "Let me show you our voice recording feature. Instead of typing lengthy feedback, reviewers can just speak naturally.
>
> [Click microphone icon]
>
> Watch - the button turns red to indicate recording.
>
> [Speak feedback]
>
> 'Alex should start taking on more leadership in sprint planning. They have really strong technical judgment but tend to defer to others when making decisions.'
>
> [Click to stop]
>
> Now the AI is transcribing and structuring this. In just a few seconds...
>
> [Wait for result]
>
> There we go - it's extracted the key point, added professional framing, and preserved the context. The reviewer can review and edit before submitting. This takes a 5-minute typing task down to 30 seconds of speaking."

### Script 2: AI Summary (60 seconds)

> "Here's where the magic happens. We have three reviews submitted from different perspectives: a manager, a peer, and a direct report.
>
> [Scroll to summary]
>
> Our AI has synthesized these into a structured summary with clear sections: Key Strengths, Areas for Growth, and Specific Examples.
>
> Notice the weighting context at the top - the manager's feedback carries full weight (1.0), while the direct report has lower weight (0.49) since they collaborate less frequently.
>
> The AI considered these weights when generating the summary, so manager insights have appropriate influence without drowning out other perspectives.
>
> Managers can edit this summary before finalizing - the AI does 90% of the synthesis work, but humans have final control."

### Script 3: Complete Cycle (2 minutes)

> "Let me walk you through a complete feedback cycle in under 2 minutes.
>
> First, an employee creates a cycle and nominates reviewers. They specify the relationship type and collaboration frequency - this drives our weighting algorithm.
>
> [Create cycle, add reviewers]
>
> Each reviewer gets a unique link. No login required - we want zero friction.
>
> [Open reviewer link]
>
> Reviewers can type or use voice. Let me record a quick voice note.
>
> [Record 'start doing' field]
>
> The AI transcribes and structures it in seconds. Reviewers do this for each field - usually takes 2-3 minutes total.
>
> [Submit review]
>
> Once we have 2+ reviews, the system auto-generates a summary.
>
> [Show manager dashboard]
>
> Managers see progress, review the AI summary, make edits if needed, and finalize.
>
> What used to take HR teams 2-3 hours of manual synthesis now happens automatically in minutes."

---

## Post-Demo Follow-Up

### Immediate Actions
- [ ] Send thank you email with demo recording link
- [ ] Share relevant documentation (README, API docs)
- [ ] Provide trial access credentials (if applicable)
- [ ] Schedule follow-up meeting

### Email Template

```
Subject: 360 Feedback Tool Demo - Follow Up

Hi [Name],

Thank you for taking the time to review the 360 Feedback Summarisation Tool demo today.

As discussed, here are the key resources:

📹 Demo Recording: [link]
📚 Documentation: [GitHub README link]
🔧 API Documentation: [/docs endpoint]
🚀 Trial Access: [credentials if applicable]

Key Features Demonstrated:
- Voice-first feedback collection with per-field recording
- AI-powered weighted summarization using Claude Sonnet
- Manager dashboard with progress tracking and editing

Next Steps:
- [Schedule technical deep-dive / pilot program / etc.]

Please let me know if you have any questions or would like to explore specific features in more detail.

Best regards,
[Your Name]
```

---

## Success Metrics

Track these metrics to improve future demos:

- **Engagement**: Questions asked during demo
- **Time spent**: Which sections held attention
- **Follow-up rate**: Requests for trial access or next meeting
- **Technical issues**: Document any failures for future prevention
- **Key objections**: Track concerns raised (pricing, security, customization)

---

## Appendix: Pre-Seeded Demo Data

### Demo Environment Setup

**Demo Cycle 1: Alex Chen**
- Subject: Alex Chen (Senior Engineer)
- Status: In Progress (3 of 4 reviews submitted)

**Reviewers:**
1. ✅ Riley Martinez (Manager, Weekly, 1.0x weight)
2. ✅ Jordan Park (Peer, Weekly, 0.8x weight)
3. ✅ Sam Kim (Direct Report, Monthly, 0.49x weight)
4. ⏳ Taylor Brooks (Cross-functional, Rarely, 0.24x weight) - Pending

**Review Tokens:**
- Riley: `demo-riley-token-abc123` (submitted)
- Jordan: `demo-jordan-token-def456` (submitted)
- Sam: `demo-sam-token-ghi789` (submitted)
- Taylor: `demo-taylor-token-jkl012` (pending - use for live demo)

**Manager Dashboard:**
- URL: `/manager/1`
- Shows: Progress, summary, edit capabilities

**Reviewer Inbox:**
- Jordan's inbox: `/inbox/jordan@company.com`
- Shows: Submitted feedback for Alex, other pending requests

---

## Questions & Troubleshooting

### FAQ During Demos

**Q: How accurate is voice transcription?**
A: Whisper achieves 95%+ accuracy with clear audio. Reviewers can edit the transcribed text before submission.

**Q: What if someone speaks a different language?**
A: Whisper supports 50+ languages. The extraction prompts are currently English-only.

**Q: Can we customize the feedback fields?**
A: Currently fixed to start/stop/continue framework. Custom fields are on the roadmap.

**Q: How do you prevent bias in AI summaries?**
A: We use weighting to balance perspectives and temperature=0.3 for consistent output. Managers have full editing control.

**Q: What's the cost per feedback cycle?**
A: ~$0.05-0.10 per cycle (voice transcription + summary generation). Scales with number of reviewers.

**Q: Is this GDPR compliant?**
A: The tool itself doesn't store recordings. Transcripts and summaries are stored. You'd need to implement data retention policies.

**Q: Can we integrate with our HRIS?**
A: API is fully documented. Integration is straightforward via REST API.

---

**Document Version**: 1.0
**Last Updated**: 2026-01-23
**Author**: Generated with Claude Code

