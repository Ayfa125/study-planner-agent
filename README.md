# Study Planner Agent - Concierge Track

An autonomous Study Planner agent designed to help users build, optimize, and review their daily study schedules. This project represents the final Capstone submission for the Google x Kaggle AI Agents Intensive.

## 🤖 What the Agent Does
The Study Planner Agent functions as a highly tailored concierge system. It takes user constraints—specifically available study hours, current skill expertise level, and a target topic (e.g., Python, Machine Learning)—and processes them through a multi-node execution graph. It algorithmically divides available hours into optimal theory and practical chunks, calls the Gemini LLM to attach curated free learning resources with explicit contextual justifications for each block, and implements a human-in-the-loop validation gate before finalizing the agenda.

## 🛠️ ADK 2.0 Concepts Demonstrated
This agent transitions completely away from legacy 1.x sequential styles, utilizing the cutting-edge **Google ADK 2.0 Graph Workflow API**:
*   **Graph Workflow Engine:** Utilizes an explicit `Workflow` state machine mapping out deterministic steps with typed schema state tracking.
*   **Function Nodes:** Built using decoupled `@node` architecture (`schedule_builder`, `resource_suggester`) to separate programmatic math scheduling logic from generative tasks.
*   **LLM Node Integration:** Integrates `gemini-2.0-flash` to query and parse external study aids dynamically based on changing user states.
*   **Human-in-the-Loop (`RequestInput`):** Halts workflow execution at a strategic breakpoint layout, printing out the prospective schedule and prompting for explicit user modification or approval.
*   **Multi-step Reasoning:** Implements a state container (`StudyPlannerState`) that updates and flows safely across nodes.

## 🚀 Setup & Execution Instructions

### Prerequisites
*   Python 3.14+
*   `uv` package manager installed

### Installation
1. Clone this repository to your local machine.
2. Navigate to the project root directory:
   ```bash
   cd study-planner-agent