# Study Planner Agent - Concierge Track

An autonomous Study Planner agent designed to help users build, optimize, and review their daily study schedules. This project represents the final Capstone submission for the Google x Kaggle AI Agents Intensive.

## 🤖 What the Agent Does
The Study Planner Agent functions as a highly tailored concierge system. It takes user constraints—specifically available study hours, current skill expertise level, and a target topic (e.g., Python, Machine Learning)—and processes them through a multi-node execution graph. It algorithmically divides available hours into optimal theory and practical chunks, calls the Gemini LLM to attach curated free learning resources with explicit contextual justifications for each block, and implements a human-in-the-loop validation gate before finalizing the agenda.

## 🛠️ Deep-Dive: Core ADK 2.0 Concepts Demonstrated
This agent transitions completely away from legacy 1.x sequential styles, utilizing the cutting-edge **Google ADK 2.0 Graph Workflow API**:
### 1. Graph Workflow Architecture (`Workflow`)
The entire agent is managed by a centralized, explicit state machine engine (`planner_workflow`). It utilizes a strictly typed runtime container (`StudyPlannerState`) built using Pydantic. This state acts as the single source of truth, safely passing payload data, structured collections, and control flags down the execution stream as nodes complete their routines.

### 2. Isolated Function Nodes (`@node`)
The graph strictly decouples calculation logic from generative logic by implementing standalone function nodes:
* `schedule_builder`: A deterministic node executing pure Python code. It handles time splits without LLM interference to ensure reliable data formatting.
* `resource_suggester`: A generative node that isolates external infrastructure calling.

### 3. Integrated LLM Node (`gemini-2.0-flash`)
Inside the `resource_suggester` node, the agent leverages the latest `google-genai` SDK to interact with the `gemini-2.0-flash` model. The node injects the current state data into structural system prompts, enforces a strict output layout style, parses out raw text fields, and saves live hyperlink elements back into the state array dynamically.

### 4. Human-in-the-Loop (`RequestInput`)
Instead of allowing the agent to run blindly to completion, the system transitions from Node 2 into a formal `human_review` breakpoint gate. By returning a `RequestInput` object, the execution loop actively pauses, formats the current proposed schedule layout, and hands control back to the operator via the terminal. The graph cannot conclude until a human enters validation or feedback.

### 5. Multi-Step State Reasoning
The flow proves multi-step state progression:
[Input State] ──► [schedule_builder] ──► [resource_suggester] ──► [human_review Gate] ──► [Final State]

## 🚀 Setup & Local Execution Instructions

### Prerequisites
*   Python: Version 3.14+ installed locally.
*   Package Manager: uv toolchain installed for ultra-fast, isolated dependency management.

### Installation
1. Clone the Repository \
Clone this repository to your local workspace and navigate to the project root directory: \
git clone [https://github.com/Ayfa125/study-planner-agent.git](https://github.com/Ayfa125/study-planner-agent.git)
cd study-planner-agent
2. Environment Dependencies Configuration: \
Use uv to automatically provision an isolated virtual environment and synchronize the mandatory structural libraries: \
uv add google-adk python-dotenv google-genai pydantic
3. Set up Your API Authentication \
Create a secure local configuration file named .env in the root of the project directory: \
New-Item -Path .env -ItemType File \
Open the .env file and append your free Gemini API token obtained from Google AI Studio: \
GOOGLE_API_KEY=your_actual_api_key_here 
4. Launch the Agent \
Execute the local standalone pipeline wrapper directly using the uv run mechanism: \
uv run app/run_local.py 

