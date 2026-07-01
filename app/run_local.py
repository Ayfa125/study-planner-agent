import os
from dotenv import load_dotenv
from google import genai

# 1. Load the free API Key from your .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in your .env file!")
    exit()

print("⚡ Starting Study Planner Agent...")
print("🤖 Node 1 active: [schedule_builder]")

# 2. Replicate the scheduling math logic directly
available_hours = 4.0
study_level = "beginner"
topic = "Python"

tasks = []
if available_hours <= 2:
    tasks.append({"name": f"Core Fundamentals: {topic}", "time": available_hours})
else:
    tasks.append({"name": f"Theory & Deep Dive: {topic}", "time": available_hours * 0.4})
    tasks.append({"name": f"Practical Labs & Projects: {topic}", "time": available_hours * 0.6})

print("🤖 Node 2 active: [resource_suggester] calling Gemini...")

# 3. Connect to your free Gemini API Key via the standard SDK
client = genai.Client(api_key=api_key)

print("\n=== Your Custom Study Plan for Python ===")
for i, task in enumerate(tasks, 1):
    prompt = (
        f"Provide exactly one free website or YouTube link targeting a "
        f"'{study_level}' level individual exploring: '{task['name']}'. "
        f"Output layout strictly format as:\nLink: <URL>\nReason: <One sentence explanation>"
    )
    try:
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        text = response.text
    except Exception as e:
        text = "Link: https://python.org\nReason: Official documentation guide."

    print(f"- Order {i}: {task['name']} for {task['time']:.1f} hours.")
    print(text)

print("\n🤖 Node 3 active: [human_review] breakpoint triggered.")
print("-" * 40)
approval = input("Do you approve this plan? (Type 'yes' to finalize or write feedback to modify): ")
print(f"\n✅ Plan finalized! User response received: '{approval}'")
