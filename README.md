# 360 Feedback Summarisation Tool

A modern web application for collecting, weighting, and summarizing 360-degree feedback with AI-powered insights. Built for managers and HR teams who need structured, actionable feedback summaries.

## Features

### Core Functionality
- **Feedback Collection**: Structured feedback forms with start/stop/continue framework
- **Voice Recording**: Browser-based voice input with automatic transcription (Whisper) and structuring (Claude)
- **Intelligent Weighting**: Automatic feedback weighting based on relationship type and collaboration frequency
- **AI-Powered Summaries**: Automated summary generation using Claude Sonnet with weighted context
- **Manager Dashboard**: Review progress tracking, summary editing, and finalization workflow
- **Reviewer Inbox**: Centralized view of all pending feedback requests

### Voice Recording Capabilities
- **Per-field recording**: Individual microphone buttons for each feedback field
- **Real-time transcription**: OpenAI Whisper API for accurate speech-to-text
- **Smart extraction**: Claude Haiku structures raw transcripts into actionable feedback
- **Interactive UI**: Visual feedback with recording indicators and processing states

## Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [PostgreSQL](https://www.postgresql.org/) - Production database
- [SQLite](https://www.sqlite.org/) - Local development database

**AI Services**
- [Claude API](https://www.anthropic.com/claude) - Feedback summarization (Sonnet 4.5)
- [OpenAI Whisper](https://openai.com/research/whisper) - Voice transcription

**Frontend**
- Vanilla JavaScript (no framework)
- Static HTML/CSS with modern browser APIs
- MediaRecorder API for audio capture

**Deployment**
- [Vercel](https://vercel.com/) - Serverless deployment platform

## Architecture

### User Flows

```
1. Employee Flow
   └─ Create feedback cycle
   └─ Nominate 3-6 reviewers
   └─ Specify relationship type & frequency
   └─ Distribute unique review links

2. Reviewer Flow
   └─ Access review via unique token link
   └─ Submit feedback (typed or voice recorded)
      ├─ Start doing (new behaviors)
      ├─ Stop doing (behaviors to change)
      ├─ Continue doing (strengths)
      ├─ Specific example
      └─ Additional comments

3. System Flow
   └─ Monitor review submissions
   └─ When 2+ reviews submitted:
      ├─ Calculate reviewer weights
      ├─ Generate AI summary
      └─ Notify manager

4. Manager Flow
   └─ View feedback progress
   └─ Review AI-generated summary
   └─ Edit summary if needed
   └─ Finalize for delivery
```

### Weighting Algorithm

Feedback is weighted based on two factors:

**Relationship Weight**
- Manager: 1.0
- Peer: 0.8
- Direct Report: 0.7
- Cross-functional: 0.6

**Frequency Weight**
- Weekly: 1.0
- Monthly: 0.7
- Rarely: 0.4

**Combined Weight** = `relationship_weight × frequency_weight`

Higher-weighted feedback has more influence in the AI-generated summary.

### Data Model

```
users
├─ id, email, name, role

feedback_cycles
├─ id, subject_user_id, created_by_user_id
├─ status, created_at, finalized_at

reviewers
├─ id, cycle_id, email, name
├─ relationship, frequency, token
└─ invited_at

reviews
├─ id, reviewer_id
├─ start_doing, stop_doing, continue_doing
├─ example, additional
└─ submitted_at

summaries
├─ id, cycle_id, content
├─ generated_at, finalized
└─ finalized_at
```

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 14+ (production) or SQLite (local development)
- OpenAI API key (for voice transcription)
- Anthropic API key (for AI summaries)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/360-feedback-tool.git
   cd 360-feedback-tool
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   OPENAI_API_KEY=sk-your-key-here
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

5. **Initialize database**
   ```bash
   # For local development (SQLite)
   python -m app.database

   # For production (PostgreSQL)
   # Run migrations from app/database.py
   ```

6. **Seed demo data (optional)**
   ```bash
   python scripts/seed_demo_data.py
   ```

### Running Locally

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage

### Creating a Feedback Cycle

1. Navigate to the employee dashboard
2. Enter employee details and create a new cycle
3. Add reviewers with their:
   - Email and name
   - Relationship type (Manager, Peer, Direct Report, Cross-functional)
   - Collaboration frequency (Weekly, Monthly, Rarely)
4. System generates unique review links for each reviewer

### Submitting Feedback

**Option 1: Type Feedback**
1. Open unique review link
2. Fill in each feedback field
3. Submit form

**Option 2: Voice Record Feedback**
1. Open unique review link
2. Click microphone icon next to any field
3. Grant microphone permission (first time)
4. Speak your feedback
5. Click again to stop recording
6. Wait for transcription and extraction
7. Review and edit the populated text
8. Submit form

### Reviewing Summary

1. Navigate to manager dashboard
2. View cycle progress (X of Y reviews submitted)
3. Once 2+ reviews submitted, view AI-generated summary
4. Edit summary if needed
5. Click "Finalize" to mark as complete

## API Endpoints

### Authentication
```
POST   /api/auth/login        # User login
POST   /api/auth/logout       # User logout
GET    /api/auth/me           # Current user info
```

### Feedback Cycles
```
GET    /api/cycles            # List all cycles
POST   /api/cycles            # Create new cycle
GET    /api/cycles/{id}       # Get cycle details
POST   /api/cycles/{id}/reviewers  # Add reviewers to cycle
```

### Reviews
```
GET    /api/review/{token}                    # Get review context
POST   /api/review/{token}                    # Submit review
POST   /api/review/{token}/voice-transcribe   # Transcribe voice feedback
```

### Manager Dashboard
```
GET    /api/manager/{cycle_id}                # Get cycle dashboard
PUT    /api/manager/{cycle_id}/summary        # Update summary
POST   /api/manager/{cycle_id}/finalize       # Finalize cycle
```

### Inbox
```
GET    /api/inbox/{email}     # Get pending reviews for email
```

## Voice Transcription API

### Endpoint
```
POST /api/review/{token}/voice-transcribe
```

### Parameters
- `audio_file` (required): Audio file (WebM format, max 10MB)
- `field_name` (optional): Specific field to extract (`start_doing`, `stop_doing`, `continue_doing`, `example`, `additional`)

### Response

**With field_name** (per-field extraction):
```json
{
  "field_value": "Consider delegating more technical decisions to senior team members..."
}
```

**Without field_name** (legacy, all fields):
```json
{
  "start_doing": "...",
  "stop_doing": "...",
  "continue_doing": "...",
  "example": "...",
  "additional": "..."
}
```

### Cost Estimation
- Voice transcription: ~$0.006 per minute (Whisper)
- Text extraction: ~$0.001 per extraction (Claude Haiku)
- **Total per recording**: ~$0.02 for 3-minute recording

## Development

### Project Structure
```
360-feedback-tool/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection & schema
│   ├── models.py            # Pydantic models
│   ├── routes/              # API route handlers
│   │   ├── auth.py
│   │   ├── cycles.py
│   │   ├── review.py
│   │   ├── manager.py
│   │   └── inbox.py
│   └── services/
│       └── summarisation.py # AI summary generation
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   ├── index.html
│   ├── dashboard.html
│   ├── review.html
│   ├── manager.html
│   └── inbox.html
├── requirements.txt
├── .env.example
└── README.md
```

### Code Quality

**Linting**
```bash
# Install dev dependencies
pip install black flake8 mypy

# Format code
black app/

# Lint
flake8 app/

# Type check
mypy app/
```

**Testing**
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

For production schema changes:
1. Update schema in `app/database.py`
2. Create migration script in `migrations/`
3. Apply migration:
   ```bash
   python migrations/001_add_new_column.py
   ```

## Deployment

### Vercel Deployment

The application is configured for Vercel serverless deployment:

1. **Connect repository to Vercel**
   ```bash
   vercel
   ```

2. **Configure environment variables**
   - Add `ANTHROPIC_API_KEY`
   - Add `OPENAI_API_KEY`
   - Add `DATABASE_URL` (use Vercel Postgres or external)

3. **Deploy**
   ```bash
   vercel --prod
   ```

### Environment Variables

Required for production:
- `ANTHROPIC_API_KEY`: Claude API key for summaries
- `OPENAI_API_KEY`: OpenAI API key for voice transcription
- `DATABASE_URL`: PostgreSQL connection string

Optional:
- `ENVIRONMENT`: Set to `production` for production mode
- `LOG_LEVEL`: Logging level (default: `INFO`)

### Database Setup (Production)

Use Vercel Postgres or any PostgreSQL provider:

```bash
# Create database
createdb feedback_360

# Run schema
psql feedback_360 < app/database.py

# Or use DATABASE_URL
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
python -m app.database
```

## Performance Considerations

### Summary Generation
- Summaries are generated asynchronously via background tasks
- Typically takes 3-5 seconds for 4-6 reviews
- Uses Claude Sonnet 4.5 (balanced speed/quality)
- Auto-regenerates when new reviews are submitted

### Voice Transcription
- Average processing time: 5-10 seconds for 1-minute recording
- Maximum recording length: 2 minutes per field
- Supported format: WebM with Opus codec
- Client-side compression for faster upload

### Caching
- No caching implemented (MVP)
- Future: Cache summaries until reviews change
- Future: Cache reviewer context by token

## Security Notes

⚠️ **This is an MVP prototype** - Not production-ready for sensitive data

### Current Limitations
- No user authentication (token-based access only)
- No rate limiting
- No audit logging
- API keys stored in environment variables
- No encryption at rest

### Production Recommendations
- Add authentication (OAuth, JWT, etc.)
- Implement rate limiting (per-user, per-IP)
- Add audit logging for all actions
- Encrypt sensitive data at rest
- Use secret management service (AWS Secrets Manager, etc.)
- Add CORS restrictions
- Implement CSRF protection

## Troubleshooting

### Voice recording not working
- Check browser compatibility (Chrome, Edge, Safari 14.1+)
- Verify microphone permissions granted
- Check `OPENAI_API_KEY` is valid
- Ensure audio file < 10MB

### Summary not generating
- Verify `ANTHROPIC_API_KEY` is valid
- Check at least 2 reviews submitted
- Check server logs for API errors
- Verify database connection

### Database connection errors
- Check `DATABASE_URL` format
- Verify PostgreSQL is running
- Check firewall rules for remote connections

## Contributing

This is a prototype project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/changes

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code)
- Powered by [Anthropic Claude](https://www.anthropic.com/claude) and [OpenAI Whisper](https://openai.com/research/whisper)
- Deployed on [Vercel](https://vercel.com/)

## Support

For issues, questions, or feature requests, please [open an issue](https://github.com/yourusername/360-feedback-tool/issues).

---

**Note**: This is a prototype MVP built for demonstration purposes. For production use, implement proper authentication, security hardening, and data protection measures.
