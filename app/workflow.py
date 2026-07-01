import os
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from google.adk import Workflow, RequestInput, node
from google import genai
from google.genai import types

# Define our structured data states matching the prompt
class StudyPlanInput(BaseModel):
    available_hours: float
    study_level: str  # beginner, intermediate, advanced
    topic: str

class StudyTask(BaseModel):
    task_name: str
    duration_hours: float
    order: int
    resource_link: Optional[str] = None
    resource_reason: Optional[str] = None

class StudyPlannerState(BaseModel):
    user_input: Optional[StudyPlanInput] = None
    schedule: List[StudyTask] = []
    is_confirmed: bool = False
    feedback: Optional[str] = None

# Initialize the workflow graph engine
planner_workflow = Workflow(name="study_planner_workflow", state_type=StudyPlannerState)

# Node 1: schedule_builder (Pure Python scheduling logic)
@node
def schedule_builder(state: StudyPlannerState) -> StudyPlannerState:
    inp = state.user_input
    if not inp:
        return state
        
    # Math logic to split available hours into parts based on input criteria
    hours = inp.available_hours
    tasks = []
    
    if hours <= 2:
        tasks.append(StudyTask(task_name=f"Core Fundamentals: {inp.topic}", duration_hours=hours, order=1))
    else:
        # Split hours logically into Theory and Practice segments
        tasks.append(StudyTask(task_name=f"Theory & Deep Dive: {inp.topic}", duration_hours=hours * 0.4, order=1))
        tasks.append(StudyTask(task_name=f"Practical Labs & Projects: {inp.topic}", duration_hours=hours * 0.6, order=2))
        
    state.schedule = tasks
    return state

# Node 2: resource_suggester (LLM node utilizing gemini-2.0-flash via global key configuration)
@node
def resource_suggester(state: StudyPlannerState) -> StudyPlannerState:
    # Set up client explicitly utilizing the GOOGLE_API_KEY from your local .env context
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    updated_schedule = []
    for task in state.schedule:
        prompt = (
            f"Provide exactly one free website, documentation page, or YouTube link targeting a "
            f"'{state.user_input.study_level}' level individual exploring the theme: '{task.task_name}'. "
            f"Output your choice strictly formatted in this layout:\n"
            f"Link: <URL>\n"
            f"Reason: <One sentence explanation why it is high value>"
        )
        
        try:
            # Explicit call targeting gemini-2.0-flash as outlined in configuration guidelines
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
            )
            text = response.text
            
            # Simple parser extraction strings
            link = "https://python.org"
            reason = "Official documentation source offering premier guidance."
            for line in text.split('\n'):
                if line.startswith("Link:"): link = line.replace("Link:", "").strip()
                if line.startswith("Reason:"): reason = line.replace("Reason:", "").strip()
                
            task.resource_link = link
            task.resource_reason = reason
        except Exception:
            # Safe Fallback values if API calls fail
            task.resource_link = "https://google.dev"
            task.resource_reason = "Google API Hub covering core framework capabilities."
            
        updated_schedule.append(task)
        
    state.schedule = updated_schedule
    return state

# Node 3: human_review (ADK 2.0 Human-in-the-loop mechanism utilizing RequestInput)
@node
def human_review(state: StudyPlannerState) -> RequestInput:
    summary = f"\n=== Your Custom Study Plan for {state.user_input.topic} ===\n"
    for task in state.schedule:
        summary += f"- Order {task.order}: {task.task_name} for {task.duration_hours:.1f} hours.\n"
        summary += f"  Resource: {task.resource_link}\n"
        summary += f"  Why: {task.resource_reason}\n"
        
    summary += "\nDo you approve this plan? (Type 'yes' to finalize or write your feedback to change it): "
    
    # Pauses the graph, prints the data output layout, and expects user terminal input
    return RequestInput(prompt=summary)

# Define the explicit execution routes mapping function nodes to directed graph edges
planner_workflow.add_node(schedule_builder)
planner_workflow.add_node(resource_suggester)
planner_workflow.add_node(human_review)

planner_workflow.add_edge(schedule_builder, resource_suggester)
planner_workflow.add_edge(resource_suggester, human_review)
