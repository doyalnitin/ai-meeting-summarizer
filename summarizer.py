import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Initialize Gemini Client (automatically picks up GEMINI_API_KEY env variable)
client = genai.Client()

# Define the Output Data Schema
class ActionItem(BaseModel):
    task: str = Field(description="The action item or task to be completed.")
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

# Core Summarization Function
def summarize_meeting(transcript: str) -> MeetingSummary:
    prompt = f"""
    You are an expert AI executive assistant. Analyze the following meeting transcript 
    and extract a structured summary.
    
    TRANSCRIPT:
    {transcript}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MeetingSummary,
            temperature=0.2,
        ),
    )
    
    # Parse JSON output into our Pydantic schema
    return MeetingSummary.model_validate_json(response.text)

# Quick Test
if __name__ == "__main__":
    sample_transcript = """
    Alice: Alright team, let's start. Today we need to discuss the launch date for Project Titan.
    Bob: We finished the backend QA yesterday. Backend is 100% ready.
    Charlie: Frontend still has a few UI bugs on mobile devices. I need until Thursday to clear them.
    Alice: Great. So let's lock in Friday, July 24th as the official release date. Charlie, make sure mobile bugs are patched by Thursday end of day.
    Bob: I'll prepare the deployment scripts and set up monitoring alerts by Wednesday.
    Alice: Perfect. Also, we decided to allocate $5,000 extra budget for social media ads post-launch.
    """

    print("⚡ Summarizing meeting...\n")
    summary = summarize_meeting(sample_transcript)
    
    print(f"📌 {summary.title}")
    print(f"\n📝 Executive Summary:\n{summary.executive_summary}")
    
    print("\n🎯 Key Decisions:")
    for decision in summary.key_decisions:
        print(f" - {decision}")
        
    print("\n✅ Action Items:")
    for item in summary.action_items:
        print(f" - [{item.assignee}] {item.task} (Due: {item.deadline})")