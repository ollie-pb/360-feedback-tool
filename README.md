# 360 Feedback Summarisation Tool

AI-powered 360-degree feedback collection and summarization. Streamlines feedback cycles with voice recording, intelligent weighting, and automated summaries.

## Features

- **Voice Recording** - Per-field voice input with automatic transcription and structuring
- **AI Summaries** - Weighted feedback synthesis using Claude Sonnet
- **Smart Weighting** - Relationship and collaboration frequency-based prioritization
- **Manager Dashboard** - Progress tracking, summary editing, and finalization
- **Token-Based Access** - Frictionless reviewer experience (no login required)

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
