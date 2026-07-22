# 🎙️ AI Meeting Summarizer

An intelligent meeting summarizer powered by Google Gemini AI. Transform your meeting recordings, transcripts, and notes into structured, actionable summaries.

## ✨ Features

- **🎤 Audio Support**: Upload audio recordings (MP3, WAV, M4A, AAC, OGG) for AI-powered analysis
- **📄 Document Processing**: Extract insights from PDF and TXT transcript files
- **✍️ Text Input**: Paste meeting notes or transcripts directly
- **📝 Executive Summaries**: Get concise 2-3 sentence overviews
- **🎯 Key Decisions**: Automatically extracted decisions from discussions
- **✅ Action Items**: Tasks with assignees and deadlines
- **💡 Topic Breakdown**: Organized discussion points by topic
- **📥 Export Options**: Download summaries as Markdown or JSON

## 🚀 How It Works

1. **Upload or Paste Content**
   - Upload audio recordings (MP3, WAV, M4A, AAC, OGG)
   - Upload transcript documents (PDF, TXT)
   - Paste meeting notes directly into the text area

2. **AI Analysis**
   - Content is sent to Google Gemini AI for processing
   - AI analyzes the content using advanced natural language understanding
   - Structured data is extracted using Pydantic schemas

3. **Get Structured Output**
   - **Executive Summary**: High-level overview of the meeting
   - **Key Decisions**: Important decisions made during the meeting
   - **Action Items**: Tasks with responsible persons and deadlines
   - **Topic Breakdown**: Detailed discussion organized by topics

4. **Export & Share**
   - Download as Markdown for documentation
   - Download as JSON for integration with other tools

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Engine**: Google Gemini 2.5 Flash
- **Data Validation**: Pydantic
- **PDF Processing**: PyPDF
- **Language**: Python 3.10+

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini API key
- pip package manager

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nitindoyal/ai-meeting-summarizer.git
   cd ai-meeting-summarizer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Key**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
   
   Or create a `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
ai-meeting-summarizer/
├── app.py              # Main Streamlit application
├── summarizer.py       # Core summarization logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔑 Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and set it as an environment variable

## 💡 Usage Examples

### Example 1: Audio Recording
1. Click the "🎤 Upload Audio" tab
2. Upload an MP3 or WAV file of your meeting
3. Click "Generate Summary from Audio"
4. Review the structured summary

### Example 2: Text Transcript
1. Click the "✍️ Paste Text" tab
2. Paste your meeting transcript
3. Click "Generate Summary from Text"
4. Download the summary as Markdown

### Example 3: PDF Document
1. Click the "📄 Upload Transcript" tab
2. Upload a PDF containing your meeting transcript
3. Click "Generate Summary from Document"
4. Export as JSON for further processing

## 📊 Output Format

The AI generates structured summaries including:

```json
{
  "title": "Q3 Product Planning Meeting",
  "executive_summary": "Team discussed Q3 roadmap...",
  "key_decisions": [
    "Launch date set for July 24th",
    "Budget increase approved"
  ],
  "action_items": [
    {
      "task": "Fix mobile UI bugs",
      "assignee": "Charlie",
      "deadline": "Thursday EOD"
    }
  ],
  "topic_breakdown": [
    {
      "topic": "Launch Timeline",
      "key_points": ["Backend ready", "Frontend needs fixes"]
    }
  ]
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for powerful AI capabilities
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Pydantic](https://docs.pydantic.dev/) for data validation
- [PyPDF](https://pypdf.readthedocs.io/) for PDF processing

## 📞 Support

If you have any questions or issues, please open an issue on GitHub or contact the maintainers.

---

Built with ❤️ using Streamlit & Google Gemini AI
