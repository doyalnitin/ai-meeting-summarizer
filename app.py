import os
import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from pypdf import PdfReader

# Page configuration
st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 5px 5px 0 0;
        background-color: #f0f2f6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea !important;
        color: white !important;
    }
    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        width: 100%;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        opacity: 0.9;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini Client
@st.cache_resource
def get_client():
    return genai.Client()

client = get_client()

# --- Pydantic Data Schema ---
class ActionItem(BaseModel):
    task: str = Field(description="Action item or task to be completed.")
    assignee: str = Field(description="Person responsible, or 'Unassigned' if not mentioned.")
    deadline: str = Field(description="Due date or timeframe, or 'TBD' if unspecified.")

class TopicSummary(BaseModel):
    topic: str = Field(description="Title of the agenda topic or discussion segment.")
    key_points: list[str] = Field(description="Bullet points of key takeaways for this topic.")

class MeetingSummary(BaseModel):
    title: str = Field(description="A concise title for the meeting.")
    executive_summary: str = Field(description="2-3 sentence high-level overview of the meeting.")
    key_decisions: list[str] = Field(description="List of agreed-upon decisions or official choices.")
    action_items: list[ActionItem] = Field(description="Extracted list of actionable tasks.")
    topic_breakdown: list[TopicSummary] = Field(description="Detailed discussion broken down by topic.")

# Helper to extract text from uploaded PDF or TXT files
def extract_text_from_file(uploaded_file) -> str:
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    else:  # .txt file
        return uploaded_file.read().decode("utf-8")

# --- Processing Function ---
def process_meeting_input(contents: list) -> MeetingSummary:
    prompt = """
    You are an expert AI executive assistant. Analyze the provided meeting recording or transcript 
    and extract a structured summary.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt] + contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MeetingSummary,
            temperature=0.2,
        ),
    )
    return MeetingSummary.model_validate_json(response.text)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🎙️ AI Meeting Summarizer")
    st.markdown("---")
    st.markdown("### ℹ️ How it works")
    st.markdown("""
    1. Upload or paste your meeting transcript
    2. AI analyzes the content
    3. Get structured summary with:
       - Executive summary
       - Key decisions
       - Action items
       - Topic breakdown
    """)
    st.markdown("---")
    st.markdown("### 🔑 Supported Formats")
    st.markdown("""
    - **Audio:** MP3, WAV, M4A, AAC, OGG
    - **Documents:** PDF, TXT
    - **Text:** Direct paste
    """)
    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    - Google Gemini AI
    - Streamlit
    - Pydantic
    - PyPDF
    """)

# --- Main Header ---
st.markdown("""
<div class="main-header">
    <h1>🎙️ AI Meeting Summarizer</h1>
    <p>Transform your meetings into actionable insights with AI-powered analysis</p>
</div>
""", unsafe_allow_html=True)

# --- Feature Cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📝 Smart Summaries</h4>
        <p>Get concise executive summaries of your meetings</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>✅ Action Items</h4>
        <p>Automatically extract tasks with assignees and deadlines</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Topic Breakdown</h4>
        <p>Organized discussion points by topic</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Input Tabs ---
tab_audio, tab_file, tab_text = st.tabs([
    "🎤 Upload Audio", 
    "📄 Upload Transcript", 
    "✍️ Paste Text"
])

contents_to_process = []
should_process = False

# 1. Audio Upload Tab
with tab_audio:
    st.markdown("### 🎤 Upload Audio Recording")
    st.markdown("Upload your meeting recording for AI-powered analysis.")
    uploaded_audio = st.file_uploader(
        "Choose an audio file", 
        type=["mp3", "wav", "m4a", "aac", "ogg"],
        help="Supported formats: MP3, WAV, M4A, AAC, OGG"
    )
    if uploaded_audio:
        st.markdown("#### 🎵 Audio Preview")
        st.audio(uploaded_audio, format=uploaded_audio.type)
        st.success(f"✅ Loaded: **{uploaded_audio.name}** ({uploaded_audio.size/1024:.1f} KB)")
        if st.button("🚀 Generate Summary from Audio", type="primary", key="btn_audio", use_container_width=True):
            audio_data = types.Part.from_bytes(
                data=uploaded_audio.read(),
                mime_type=uploaded_audio.type,
            )
            contents_to_process = [audio_data]
            should_process = True

# 2. PDF / TXT File Tab
with tab_file:
    st.markdown("### 📄 Upload Transcript Document")
    st.markdown("Upload a PDF or TXT file containing your meeting transcript.")
    uploaded_doc = st.file_uploader(
        "Choose a document", 
        type=["pdf", "txt"],
        help="Supported formats: PDF, TXT"
    )
    if uploaded_doc:
        st.success(f"✅ Loaded: **{uploaded_doc.name}** ({uploaded_doc.size/1024:.1f} KB)")
        if st.button("🚀 Generate Summary from Document", type="primary", key="btn_doc", use_container_width=True):
            extracted_text = extract_text_from_file(uploaded_doc)
            if extracted_text.strip():
                contents_to_process = [extracted_text]
                should_process = True
            else:
                st.error("❌ Could not extract any readable text from this file.")

# 3. Paste Text Tab
with tab_text:
    st.markdown("### ✍️ Paste Meeting Transcript")
    st.markdown("Paste your meeting notes or transcript directly.")
    transcript_text = st.text_area(
        "Enter your meeting transcript here:", 
        height=250,
        placeholder="Paste your meeting transcript, notes, or discussion here..."
    )
    if st.button("🚀 Generate Summary from Text", type="primary", key="btn_text", use_container_width=True):
        if transcript_text.strip():
            contents_to_process = [transcript_text]
            should_process = True
        else:
            st.warning("⚠️ Please paste a transcript before submitting.")

# --- Processing & Output Section ---
if should_process and contents_to_process:
    with st.spinner("🔄 Analyzing meeting content with Gemini AI..."):
        try:
            summary = process_meeting_input(contents_to_process)
            
            st.markdown("---")
            
            # Title Section
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1.5rem;">
                <h2 style="margin: 0; color: white;">📌 {summary.title}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Executive Summary Card
            st.markdown("### 📝 Executive Summary")
            st.info(summary.executive_summary)
            
            # Two Column Layout for Decisions and Actions
            col1, col2 = st.columns(2)
            
            # Key Decisions
            with col1:
                st.markdown("### 🎯 Key Decisions")
                for i, decision in enumerate(summary.key_decisions, 1):
                    st.markdown(f"""
                    <div style="background: #f0f7ff; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #667eea;">
                        <strong>{i}.</strong> {decision}
                    </div>
                    """, unsafe_allow_html=True)
                    
            # Action Items
            with col2:
                st.markdown("### ✅ Action Items")
                for item in summary.action_items:
                    st.markdown(f"""
                    <div style="background: #f0fff4; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #48bb78;">
                        <strong>📋 {item.task}</strong><br>
                        <small>👤 <code>{item.assignee}</code> | 📅 <code>{item.deadline}</code></small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Topic Breakdown
            st.markdown("---")
            st.markdown("### 💡 Topic Breakdown")
            for topic in summary.topic_breakdown:
                with st.expander(f"📌 {topic.topic}", expanded=True):
                    for point in topic.key_points:
                        st.markdown(f"""
                        <div style="padding: 0.3rem 0; border-bottom: 1px solid #eee;">
                            • {point}
                        </div>
                        """, unsafe_allow_html=True)

            # Export Section
            st.markdown("---")
            st.markdown("### 📥 Export Summary")
            
            # Generate different export formats
            markdown_export = f"# {summary.title}\n\n## Executive Summary\n{summary.executive_summary}\n\n## Key Decisions\n"
            markdown_export += "\n".join([f"- {d}" for d in summary.key_decisions])
            markdown_export += "\n\n## Action Items\n"
            markdown_export += "\n".join([f"- [{item.assignee}] {item.task} (Due: {item.deadline})" for item in summary.action_items])
            markdown_export += "\n\n## Topic Breakdown\n"
            for topic in summary.topic_breakdown:
                markdown_export += f"\n### {topic.topic}\n"
                markdown_export += "\n".join([f"- {point}" for point in topic.key_points])
            
            # JSON export
            import json
            json_export = json.dumps(summary.model_dump(), indent=2)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download as Markdown",
                    data=markdown_export,
                    file_name=f"{summary.title.lower().replace(' ', '_')}_summary.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_export,
                    file_name=f"{summary.title.lower().replace(' ', '_')}_summary.json",
                    mime="application/json",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Error processing meeting: {str(e)}")
            st.info("💡 Make sure you have set up your GEMINI_API_KEY environment variable.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>Built with ❤️ using Streamlit & Google Gemini AI</p>
    <small>AI Meeting Summarizer - Transform your meetings into actionable insights</small>
</div>
""", unsafe_allow_html=True)
