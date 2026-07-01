# ruff: noqa
# Copyright 2026 Google LLC
import os
from pydantic import BaseModel
from typing import List, Optional
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google import genai
from dotenv import load_dotenv

# 1. Load local environment credentials (.env)
load_dotenv()

# 2. Define standard input schema for the playground tool inspector
class StudyPlanInput(BaseModel):
    available_hours: float
    study_level: str  # beginner, intermediate, advanced
    topic: str

# Tool 1: schedule_builder
def schedule_builder(available_hours: float, study_level: str, topic: str) -> str:
    """Generates a structured daily study plan schedule by dividing hours mathematically."""
    hours = float(available_hours)
    summary = f"\n=== Your Custom Study Plan for {topic} ({study_level}) ===\n"
    
    if hours <= 2:
        summary += f"- Step 1: Core Fundamentals for {hours:.1f} hours.\n"
    else:
        summary += f"- Step 1: Theory & Deep Dive for {hours * 0.4:.1f} hours.\n"
        summary += f"- Step 2: Practical Labs & Projects for {hours * 0.6:.1f} hours.\n"
        
    return summary

# Tool 2: resource_suggester
def resource_suggester(topic: str, study_level: str) -> str:
    """Uses Gemini LLM to suggest one free learning link with a short reason why it is helpful."""
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    prompt = (
        f"Provide exactly one free high-quality learning website or YouTube link for a "
        f"'{study_level}' level individual studying '{topic}'. "
        f"Format as: Link: <URL> - Reason: <One sentence summary>"
    )
    try:
        # Updated to standard 2.5 flash identifier to clear the 404 endpoint routing error
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text
    except Exception:
        return "Link: https://python.org - Reason: Official documentation and guide portal."

# Tool 3: human_review
def human_review(plan_details: str) -> str:
    """Displays the finalized agenda layout to the user for interactive confirmation."""
    return f"PROMPT_USER: Please review and approve this generated study plan structure:\n{plan_details}"

# 3. Define standard root agent configuration with explicit structural tools
root_agent = Agent(
    name="root_agent",
    model=Gemini(model="gemini-2.5-flash"), # Updated to standard production 2.5 flash identifier
    instruction=(
        "You are the Study Planner Concierge. You must assist the user step-by-step: "
        "1. Execute 'schedule_builder' to calculate the split. "
        "2. Execute 'resource_suggester' to fetch reference material links. "
        "3. Output the combined overview to the user using the 'human_review' tool for approval."
    ),
    tools=[schedule_builder, resource_suggester, human_review]
)

# 4. Bind the agent frame securely
app = App(
    name="app",
    root_agent=root_agent,
)
