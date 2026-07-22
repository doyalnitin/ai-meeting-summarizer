<div align="center">

# AI Meeting Summarizer

**Transform meetings into actionable insights with AI-powered analysis.**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-ff4b4b?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python)](https://python.org)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.5-4285f4?logo=google)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[Live Demo](#) · [Report Bug](https://github.com/doyalnitin/ai-meeting-summarizer/issues) · [Request Feature](https://github.com/doyalnitin/ai-meeting-summarizer/issues)

</div>

---

## What is this?

AI Meeting Summarizer is a **Streamlit web app** that uses Google Gemini AI to analyze meeting recordings, transcripts, and notes. Upload audio, paste text, or drop a PDF — get a structured summary with executive overview, key decisions, action items, and topic breakdown in seconds.

## Features

| Feature | Description |
|---------|-------------|
| **Audio Upload** | Supports MP3, WAV, M4A, AAC, OGG recordings |
| **Document Upload** | Extract text from PDF and TXT transcripts |
| **Text Input** | Paste meeting notes directly |
| **Executive Summary** | 2-3 sentence high-level overview |
| **Key Decisions** | Auto-extracted decisions from discussions |
| **Action Items** | Tasks with assignees and deadlines |
| **Topic Breakdown** | Discussion points organized by topic |
| **Export Markdown** | Download summary as `.md` file |
| **Export JSON** | Download structured data as `.json` |

## How it Works

```
┌──────────────────────────────────────────────────────────────┐
│                    INPUT METHODS                             │
├──────────────────┬──────────────────┬────────────────────────┤
│   🎤 Audio       │   📄 Document    │   ✍️ Text              │
│                  │                  │                        │
│  ┌────────────┐  │  ┌────────────┐  │  ┌──────────────────┐  │
│  │  MP3/WAV   │  │  │  PDF/TXT   │  │  │  Paste Transcript│  │
│  │  M4A/AAC   │  │  │  Upload    │  │  │  Directly        │  │
│  │  OGG       │  │  │            │  │  │                  │  │
│  └─────┬──────┘  │  └─────┬──────┘  │  └────────┬─────────┘  │
│        │         │        │         │           │             │
└────────┼─────────┴────────┼─────────┴───────────┼─────────────┘
         │                  │                     │
         └──────────────────┼─────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │    GOOGLE GEMINI AI     │
              │    (gemini-2.5-flash)   │
              │                         │
              │  • NLP Analysis         │
              │  • Entity Extraction    │
              │  • Structured Output    │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │   STRUCTURED SUMMARY    │
              ├─────────────────────────┤
              │  📌 Meeting Title       │
              │  📝 Executive Summary   │
              │  🎯 Key Decisions       │
              │  ✅ Action Items        │
              │  💡 Topic Breakdown     │
              ├─────────────────────────┤
              │  📥 Export as .md/.json  │
              └─────────────────────────┘
```

### Step 1: Choose Input Method
- **Audio**: Upload a recording (MP3, WAV, M4A, AAC, OGG)
- **Document**: Upload a PDF or TXT transcript
- **Text**: Paste meeting notes directly

### Step 2: AI Analyzes Content
Content is sent to **Gemini 2.5 Flash** which extracts structured data using Pydantic schemas for type-safe output.

### Step 3: Get Structured Output
- Executive summary for quick overview
- Key decisions made during the meeting
- Action items with responsible persons and deadlines
- Topic-wise breakdown of discussions

### Step 4: Export
Download as Markdown for documentation or JSON for integration with other tools.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Engine | Google Gemini 2.5 Flash |
| Data Validation | Pydantic |
| PDF Processing | PyPDF |
| Language | Python 3.10+ |

## Project Structure

```
ai-meeting-summarizer/
├── app.py              # Main Streamlit application
│                       #   - UI components & layout
│                       #   - File upload handling
│                       #   - Gemini API integration
│                       #   - Export functionality
├── summarizer.py       # Core summarization logic
│                       #   - Pydantic schemas
│                       #   - summarize_meeting()
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Getting Started

### Prerequisites
- Python 3.10+
- A [Gemini API key](https://aistudio.google.com/apikey) (free tier available)

### 1. Clone & Install

```bash
git clone https://github.com/doyalnitin/ai-meeting-summarizer.git
cd ai-meeting-summarizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

**Local** — create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

Or export directly:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Streamlit Cloud** — add secret in the dashboard:

1. Go to your app on [share.streamlit.io](https://share.streamlit.io)
2. Click **Manage app** → **Secrets**
3. Add:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

### 3. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## API Schema

The AI returns structured data using Pydantic models:

```python
class ActionItem(BaseModel):
    task: str          # Action item or task
    assignee: str      # Person responsible
    deadline: str      # Due date or timeframe

class TopicSummary(BaseModel):
    topic: str         # Discussion topic title
    key_points: list   # Key takeaways

class MeetingSummary(BaseModel):
    title: str              # Meeting title
    executive_summary: str  # 2-3 sentence overview
    key_decisions: list     # Decisions made
    action_items: list      # Tasks with assignees
    topic_breakdown: list   # Topic-wise breakdown
```

## Output Example

```json
{
  "title": "Q3 Product Planning Meeting",
  "executive_summary": "Team discussed Q3 roadmap and finalized launch date for July 24th.",
  "key_decisions": [
    "Launch date set for Friday, July 24th",
    "Extra $5,000 budget allocated for social media ads"
  ],
  "action_items": [
    {
      "task": "Fix mobile UI bugs",
      "assignee": "Charlie",
      "deadline": "Thursday EOD"
    },
    {
      "task": "Prepare deployment scripts",
      "assignee": "Bob",
      "deadline": "Wednesday"
    }
  ],
  "topic_breakdown": [
    {
      "topic": "Launch Timeline",
      "key_points": ["Backend is 100% ready", "Frontend needs mobile fixes"]
    }
  ]
}
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Nitin Doyal** — [Twitter](https://twitter.com/doyalnitin) · [GitHub](https://github.com/doyalnitin) · [LinkedIn](https://linkedin.com/in/doyalnitin)

---

<div align="center">

**Built with AI, designed for humans.**

</div>
