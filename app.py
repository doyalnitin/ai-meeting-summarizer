import os
import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Meeting Summarizer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    .stApp { background: #fafafa; }

    section[data-testid="stSidebar"] {
        background: #fff;
        border-right: 1px solid #f0f0f0;
    }
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #1a1a1a;
        font-weight: 600;
    }

    .block-container {
        padding-top: 2.5rem;
        max-width: 900px;
        margin: 0 auto;
    }

    .title-section {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }
    .title-section h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #0f0f0f;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .title-section p {
        color: #888;
        font-size: 1rem;
        font-weight: 400;
    }

    .pill-row {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.85rem;
        border-radius: 100px;
        font-size: 0.78rem;
        font-weight: 500;
        background: #f5f5f5;
        color: #555;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px !important;
        background: #f0f0f0 !important;
        border-radius: 12px !important;
        padding: 5px !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 0.7rem 1.5rem !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        color: #666 !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #333 !important;
        background: #e8e8e8 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #1a1a1a !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    .stFileUploader {
        border: 1px dashed #ddd;
        border-radius: 10px;
        background: #fff;
    }

    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #e8e8e8;
        background: #fff;
        font-size: 0.9rem;
    }
    .stTextArea textarea:focus {
        border-color: #1a1a1a;
        box-shadow: 0 0 0 1px #1a1a1a;
    }

    div[data-testid="stButton"] > button {
        background: #1a1a1a;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 0.55rem 1.5rem;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.15s ease;
    }
    div[data-testid="stButton"] > button:hover {
        background: #333;
        transform: translateY(-1px);
    }

    div[data-testid="stDownloadButton"] > button {
        background: #fff;
        color: #1a1a1a;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.82rem;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        border-color: #1a1a1a;
        background: #f9f9f9;
    }

    .summary-card {
        background: #fff;
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .summary-card h4 {
        margin: 0 0 0.75rem 0;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #999;
    }
    .summary-card p, .summary-card li {
        color: #333;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .decision-item {
        padding: 0.75rem 1rem;
        background: #fafafa;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 2px solid #1a1a1a;
        font-size: 0.9rem;
        color: #333;
    }

    .action-item {
        padding: 0.85rem 1rem;
        background: #fafafa;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 2px solid #10b981;
    }
    .action-item .task {
        font-weight: 500;
        color: #1a1a1a;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    .action-item .meta {
        font-size: 0.78rem;
        color: #999;
    }
    .action-item .meta span {
        background: #f0f0f0;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        margin-right: 0.4rem;
    }

    .topic-item {
        padding: 1rem 1.2rem;
        background: #fff;
        border: 1px solid #eee;
        border-radius: 10px;
        margin-bottom: 0.75rem;
    }
    .topic-item h5 {
        margin: 0 0 0.6rem 0;
        font-size: 0.92rem;
        font-weight: 600;
        color: #1a1a1a;
    }
    .topic-item ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    .topic-item li {
        font-size: 0.85rem;
        color: #666;
        line-height: 1.7;
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #bbb;
        margin-bottom: 1rem;
    }

    .stAlert { border-radius: 10px; }
    .stSpinner > div { text-align: center; }

    hr {
        border: none;
        border-top: 1px solid #f0f0f0;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    return genai.Client(api_key=api_key)

client = get_client()

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

def extract_text_from_file(uploaded_file) -> str:
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return uploaded_file.read().decode("utf-8")

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

st.markdown("""
<div class="title-section">
    <h1>AI Meeting Summarizer</h1>
    <p>Drop in a transcript, get a structured summary in seconds.</p>
    <div class="pill-row">
        <span class="pill">✦ Gemini 2.5 Flash</span>
        <span class="pill">音频 Audio</span>
        <span class="pill">📄 PDF / TXT</span>
        <span class="pill">✍️ Paste Text</span>
    </div>
</div>
""", unsafe_allow_html=True)

tab_audio, tab_file, tab_text = st.tabs(["🎤  Audio Recording", "📄  Document Upload", "✍️  Paste Transcript"])

contents_to_process = []
should_process = False

with tab_audio:
    st.markdown("")
    uploaded_audio = st.file_uploader(
        "Upload audio recording",
        type=["mp3", "wav", "m4a", "aac", "ogg"],
        label_visibility="collapsed"
    )
    if uploaded_audio:
        st.audio(uploaded_audio, format=uploaded_audio.type)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Summarize", key="btn_audio", use_container_width=True):
                audio_data = types.Part.from_bytes(
                    data=uploaded_audio.read(),
                    mime_type=uploaded_audio.type,
                )
                contents_to_process = [audio_data]
                should_process = True

with tab_file:
    st.markdown("")
    uploaded_doc = st.file_uploader(
        "Upload transcript",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )
    if uploaded_doc:
        st.markdown(f"<p style='color:#999;font-size:0.82rem;margin-top:0.5rem;'>{uploaded_doc.name}</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Summarize", key="btn_doc", use_container_width=True):
                extracted_text = extract_text_from_file(uploaded_doc)
                if extracted_text.strip():
                    contents_to_process = [extracted_text]
                    should_process = True
                else:
                    st.error("No readable text found.")

with tab_text:
    st.markdown("")
    transcript_text = st.text_area(
        "Paste transcript",
        height=220,
        placeholder="Paste your meeting transcript, notes, or discussion here...",
        label_visibility="collapsed"
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Summarize", key="btn_text", use_container_width=True):
            if transcript_text.strip():
                contents_to_process = [transcript_text]
                should_process = True
            else:
                st.warning("Please paste a transcript first.")

if should_process and contents_to_process:
    with st.spinner("Analyzing with Gemini..."):
        try:
            summary = process_meeting_input(contents_to_process)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<p class='section-label'>Result</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='font-size:1.5rem;font-weight:700;color:#0f0f0f;margin-bottom:0.25rem;'>{summary.title}</h2>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="summary-card">
                <h4>Executive Summary</h4>
                <p>{summary.executive_summary}</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                decisions_html = ""
                for i, d in enumerate(summary.key_decisions, 1):
                    decisions_html += f"<div class='decision-item'><strong>{i}.</strong> {d}</div>"
                st.markdown(f"""
                <div class="summary-card">
                    <h4>Key Decisions</h4>
                    {decisions_html}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                actions_html = ""
                for item in summary.action_items:
                    actions_html += f"""
                    <div class="action-item">
                        <div class="task">{item.task}</div>
                        <div class="meta"><span>{item.assignee}</span><span>{item.deadline}</span></div>
                    </div>
                    """
                st.markdown(f"""
                <div class="summary-card">
                    <h4>Action Items</h4>
                    {actions_html}
                </div>
                """, unsafe_allow_html=True)

            topics_html = ""
            for topic in summary.topic_breakdown:
                points = "".join([f"<li>{p}</li>" for p in topic.key_points])
                topics_html += f"""
                <div class="topic-item">
                    <h5>{topic.topic}</h5>
                    <ul>{points}</ul>
                </div>
                """

            st.markdown(f"""
            <div class="summary-card">
                <h4>Topic Breakdown</h4>
                {topics_html}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            import json
            markdown_export = f"# {summary.title}\n\n## Executive Summary\n{summary.executive_summary}\n\n## Key Decisions\n"
            markdown_export += "\n".join([f"- {d}" for d in summary.key_decisions])
            markdown_export += "\n\n## Action Items\n"
            markdown_export += "\n".join([f"- [{item.assignee}] {item.task} (Due: {item.deadline})" for item in summary.action_items])
            markdown_export += "\n\n## Topic Breakdown\n"
            for topic in summary.topic_breakdown:
                markdown_export += f"\n### {topic.topic}\n"
                markdown_export += "\n".join([f"- {point}" for point in topic.key_points])

            json_export = json.dumps(summary.model_dump(), indent=2)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download Markdown",
                    data=markdown_export,
                    file_name=f"{summary.title.lower().replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    label="Download JSON",
                    data=json_export,
                    file_name=f"{summary.title.lower().replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem 0;color:#ccc;font-size:0.78rem;">
    Built with Streamlit & Gemini AI
</div>
""", unsafe_allow_html=True)
