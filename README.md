# 360 Feedback Summarisation Tool

AI-powered 360-degree feedback collection and summarization. Streamlines feedback cycles with voice recording, intelligent weighting, and automated summaries.

## Features

- **Voice Recording** - Per-field voice input with automatic transcription and structuring
- **AI Summaries** - Weighted feedback synthesis using Claude Sonnet
- **Smart Weighting** - Relationship and collaboration frequency-based prioritization
- **Manager Dashboard** - Progress tracking, summary editing, and finalization
- **Token-Based Access** - Frictionless reviewer experience (no login required)

## What's Included

### Built (MVP Scope)
- ✅ **Feedback Collection** - Token-based review forms with start/stop/continue framework
- ✅ **Voice Recording** - Per-field voice input with Whisper transcription + Claude extraction
- ✅ **Weighted Summarization** - AI-generated summaries with relationship/frequency weighting
- ✅ **Manager Dashboard** - Progress tracking, summary editing, finalization workflow
- ✅ **Reviewer Inbox** - Centralized view of all pending reviews by email
- ✅ **Auto-regeneration** - Summaries auto-update when new reviews are submitted

### Explicitly Descoped
- ❌ **Authentication** - No login system (token-based access only)
- ❌ **Email Notifications** - Review links shared manually, no automated reminders
- ❌ **Multi-cycle Management** - One feedback cycle per employee (no historical tracking)
- ❌ **Advanced Analytics** - No reporting, trends, or comparative analysis
- ❌ **Customizable Fields** - Fixed to start/stop/continue framework
- ❌ **PDF Export** - Summaries viewable in-app only
- ❌ **Mobile Optimization** - Desktop-focused responsive design

**Rationale**: MVP focused on core workflow (collect → weight → summarize → finalize) with 6-hour timebox. Authentication, notifications, and analytics are standard features but add significant complexity for marginal MVP value.

## Tech Stack

- **Backend**: FastAPI (Python), PostgreSQL
- **AI**: Claude API (Sonnet 4.5 & Haiku), OpenAI Whisper
- **Frontend**: Vanilla JavaScript, Static HTML/CSS
- **Deployment**: Vercel (Serverless)

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL or SQLite (local dev)
- Anthropic API key
- OpenAI API key

### Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/360-feedback-tool.git
cd 360-feedback-tool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python -m app.database

# Run
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` and explore the API docs at `/docs`.

## How It Works

### 1. Employee Creates Cycle
- Nominates 3-6 reviewers
- Specifies relationship type (Manager, Peer, Direct Report, Cross-functional)
- Sets collaboration frequency (Weekly, Monthly, Rarely)
- System generates unique review links

### 2. Reviewers Submit Feedback
- Access via unique token link (no login)
- Submit typed or voice-recorded feedback:
  - Start doing (new behaviors)
  - Stop doing (behaviors to change)
  - Continue doing (strengths)
  - Specific example
  - Additional comments
- Voice recordings are transcribed and structured automatically

### 3. AI Generates Summary
- When 2+ reviews submitted, system auto-generates weighted summary
- Weighting formula: `relationship_weight × frequency_weight`
  - Manager/Weekly: 1.0 (highest influence)
  - Peer/Monthly: 0.56
  - Direct Report/Rarely: 0.28 (lowest influence)

### 4. Manager Finalizes
- Reviews AI-generated summary
- Edits if needed
- Finalizes for delivery

## How Summarization Works

The tool uses a two-stage AI pipeline for intelligent feedback synthesis:

### Stage 1: Voice Transcription (Per-Field)

**Process**: OpenAI Whisper → Claude Haiku extraction

When reviewers record voice feedback, each field is processed independently:

1. **Transcription** - Whisper converts audio to raw text (~5 seconds)
2. **Extraction** - Claude Haiku structures the transcript into professional feedback

**Example Extraction Prompt** (Start Doing field):
```
Transform this voice feedback into a constructive "Start Doing" recommendation.

Example input: "I think she could really benefit from speaking up more in
client meetings. She clearly has good ideas because I see them in her written
work, but she tends to stay quiet when the clients are in the room."

Example output: "Consider taking a more active voice in client meetings. Your
ideas come through strongly in written deliverables, and sharing them directly
during discussions would increase your visibility with clients."

Guidelines:
- Write 2-4 sentences that capture the full substance
- Frame recommendations around observable behaviors, not personality traits
- Include reasoning or potential impact if mentioned
- Use professional, encouraging language
- Preserve specific details and contexts

Transcript: "{user's spoken feedback}"
```

**Key Design Choice**: Per-field recording (not one long recording) reduces cognitive load and makes editing easier. Each field gets a focused prompt tuned for that feedback type.

### Stage 2: Weighted Summarization

**Process**: Claude Sonnet synthesizes all reviews with weighting context

**Weighting Formula**:
```
combined_weight = relationship_weight × frequency_weight

Relationship Weights:
- Manager:          1.0
- Peer:             0.8
- Direct Report:    0.7
- Cross-functional: 0.6

Frequency Weights:
- Weekly:   1.0
- Monthly:  0.7
- Rarely:   0.4

Examples:
- Manager, Weekly:           1.0 × 1.0 = 1.00 (highest influence)
- Peer, Monthly:             0.8 × 0.7 = 0.56
- Direct Report, Rarely:     0.7 × 0.4 = 0.28 (lowest influence)
```

**Summarization Prompt** (Claude Sonnet 4):
```
You are summarising 360-degree feedback for an employee performance review.

## Employee
Alex Chen

## Feedback Submissions

### Reviewer: Riley Martinez (Manager, works together weekly)
**Weight**: 1.00 (based on relationship and collaboration frequency)

**Start doing**: Consider delegating more code reviews to senior engineers...
**Stop doing**: Reduce frequency of late-night work sessions...
**Continue doing**: Your detailed technical documentation is excellent...
**Example**: During the Q3 planning meeting, they proactively identified...
**Additional**: Generally strong technical leadership...

---

### Reviewer: Jordan Park (Peer, works together weekly)
**Weight**: 0.80

[... similar structure for other reviewers ...]

## Instructions
Synthesise this feedback into a summary with these sections:
1. **Strengths** - What this person does well (weight higher-confidence
   feedback more heavily)
2. **Growth Areas** - Where they can improve
3. **Key Examples** - Specific behaviours observed (quote or paraphrase)
4. **Suggested Focus** - 1-2 priority areas for development

Weight feedback from managers and frequent collaborators more heavily than
occasional cross-functional contacts.

Keep the tone constructive and actionable. Be concise. Use markdown formatting.
```

**Model Configuration**:
- Model: `claude-sonnet-4-20250514` (balance of quality and speed)
- Max tokens: `2048` (room for detailed summaries)
- Temperature: `0.3` (consistent, professional output)

**Generated Weighting Explanation** (shown to managers):
> "This summary weights feedback based on reviewer relationship (manager feedback
> weighted highest) and collaboration frequency (weekly interactions weighted
> highest). Riley Martinez's feedback as a manager with weekly interaction
> carried the most weight."

### Why This Approach Works

**Transparency**: Weights are mathematically calculated and explained to managers, not hidden in a black box.

**Fairness**: Prevents gaming (e.g., nominating 5 junior reports to dilute critical peer feedback). Manager input always carries appropriate influence.

**Quality**: Two-stage processing (transcription → extraction, then weighted synthesis) produces more accurate results than single-pass summarization.

**Editability**: Managers can review, edit, and finalize summaries. AI does 90% of the synthesis work, humans retain control.

## Architecture

```
┌─────────────┐
│   Frontend  │  Static HTML/JS
│  (Vanilla)  │
└──────┬──────┘
       │
┌──────▼──────┐
│   FastAPI   │  Python backend
│   Backend   │
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│  PostgreSQL  │  AI Services  │
│   Database   │  Claude/Whisper│
└──────────────┴───────────────┘
```

## Deployment

### Vercel (Recommended)

```bash
vercel
```

Configure environment variables in Vercel dashboard:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `DATABASE_URL`

## API Reference

Full API documentation available at `/docs` when running.

**Key Endpoints:**
- `POST /api/cycles` - Create feedback cycle
- `POST /api/review/{token}` - Submit review
- `POST /api/review/{token}/voice-transcribe` - Transcribe voice
- `GET /api/manager/{cycle_id}` - Manager dashboard
- `GET /api/inbox/{email}` - Reviewer inbox

## Project Structure

```
app/
├── main.py              # FastAPI app
├── database.py          # Schema & connection
├── routes/              # API endpoints
└── services/            # AI summarization

static/
├── css/                 # Styles
├── js/                  # Frontend logic
└── *.html               # Pages
```

## Security Note

⚠️ **This is an MVP prototype.** For production use, implement:
- User authentication
- Rate limiting
- Audit logging
- Encryption at rest
- GDPR compliance measures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
4. Open a Pull Request

## License

MIT License - see LICENSE file for details

---

**Built with [Claude Code](https://claude.com/claude-code)** | Powered by Anthropic & OpenAI | Deployed on Vercel
