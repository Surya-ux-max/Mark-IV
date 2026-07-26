import os
from langchain_core.messages import AIMessage
from tools.calendar_tool import add_event, get_events
from groq import Groq

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "calendar_agent.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    CALENDAR_SYSTEM_PROMPT = f.read()

def run_calendar_agent(messages):
    user_query = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_query = msg.content
            break
            
    q_lower = user_query.lower()
    
    # Simple semantic rule parsing for demo
    if "schedule" in q_lower or "add event" in q_lower or "remind" in q_lower:
        # Simulate parsing a title from the query
        title = "SurveX Event"
        if "to" in q_lower:
            parts = q_lower.split("to")
            title = parts[1].strip()[:50]
        # Schedule it
        result = add_event(title, user_query, "2026-07-27 10:00:00", "2026-07-27 11:00:00")
    else:
        # List events
        events = get_events()
        if events:
            result = "Current scheduled events:\n" + "\n".join([f"- {e['title']}: {e['start_time']} ({e['description']})" for e in events[:5]])
        else:
            result = "No upcoming calendar events found."

    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {"role": "system", "content": CALENDAR_SYSTEM_PROMPT},
                {"role": "system", "content": f"Calendar Tool outputs:\n{result}"}
            ]
            for msg in messages[-3:]:
                role = "user" if msg.type == "human" else "assistant"
                llm_messages.append({"role": role, "content": msg.content})
                
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=llm_messages,
                temperature=0.3
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Calendar agent LLM error: {e}")
            
    return result
