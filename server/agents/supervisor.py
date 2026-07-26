import os
import json
from langchain_core.messages import AIMessage
from groq import Groq
from database.db import get_db_connection

# Load supervisor prompt
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "supervisor.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SUPERVISOR_SYSTEM_PROMPT = f.read()

# --- Keywords that require specialized agents ---
DOMAIN_KEYWORDS = {
    "github_agent":    ["github", "commit", "branch", "repo", "pull request", "git"],
    "weather_agent":   ["weather", "forecast", "temperature", "humidity", "rain", "wind", "climate"],
    "calendar_agent":  ["calendar", "schedule", "remind", "event", "appointment", "booking"],
    "email_agent":     ["email", "mail", "send message", "inbox", "draft"],
    "browser_cleaner": ["clean", "cache", "cookies", "clear browser", "temporary files"],
    "browser_agent":   ["search", "google", "website", "browse", "look up", "find online"],
    "coding_agent":    ["code", "script", "file", "compile", "workspace", "debug", "error"],
    "memory_agent":    ["remember", "memory", "recall", "history", "profile", "saved"],
}

def _find_unvisited_matching_agents(user_query: str, trace: list) -> list:
    """
    Scans the user query for all matching domain keywords and returns
    a list of matching agents that have NOT been visited in the trace yet.
    """
    q = user_query.lower()
    matching = []
    for agent, keywords in DOMAIN_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            if agent not in trace:
                matching.append(agent)
    return matching

def run_supervisor(messages, trace):
    """
    Supervisor Agent orchestrates execution across multiple specialized agents.
    It receives the message thread and trace history, delegates to the next unvisited
    specialized agent required by the query, and returns '__end__' once all agents complete.
    """
    user_query = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_query = msg.content
            break

    # 1. Multi-agent keyword scan: find next required unvisited agent
    unvisited = _find_unvisited_matching_agents(user_query, trace)
    if unvisited:
        return unvisited[0]

    # 2. LLM route: for complex or ambiguous multi-domain queries where keyword matching didn't trigger
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key and not any(kw_agent in trace for kw_agent in DOMAIN_KEYWORDS.keys()):
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [{"role": "system", "content": SUPERVISOR_SYSTEM_PROMPT}]
            for msg in messages[-6:]:
                role = "user" if msg.type == "human" else "assistant"
                llm_messages.append({"role": role, "content": msg.content})

            llm_messages.append({
                "role": "system",
                "content": 'Respond ONLY with a JSON object. Format: {"next": "AGENT_NAME"}. Select from: ["github_agent", "weather_agent", "browser_agent", "coding_agent", "memory_agent", "browser_cleaner", "calendar_agent", "email_agent", "__end__"]'
            })

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=llm_messages,
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=30
            )
            response_json = json.loads(completion.choices[0].message.content)
            next_agent = response_json.get("next", "__end__")
            if next_agent not in trace and next_agent != "__end__":
                return next_agent
        except Exception as e:
            print(f"Supervisor LLM routing error: {e}")

    # 3. All matching/delegated agents completed → termination
    return "__end__"


def compile_final_response(messages):
    """
    Compiles the final response. If specialized agents ran and provided output,
    return their actual agent responses directly so data is NEVER skipped, altered, or hallucinated.
    """
    user_query = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_query = msg.content
            break

    # Extract AI responses produced by specialized agents during execution trace
    agent_responses = []
    for msg in reversed(messages):
        if msg.type == "human":
            break
        if msg.type == "ai" and msg.content.strip():
            agent_responses.insert(0, msg.content.strip())

    # If specialized agent(s) ran and produced answer, return it directly!
    if agent_responses:
        return "\n\n".join(agent_responses)

    # General conversation fallback (no agent ran)
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {
                    "role": "system",
                    "content": (
                        "You are SurveX, a warm, intelligent, and natural AI assistant (inspired by JARVIS) speaking to your operator, Surya. "
                        "Respond in a warm, natural, and conversational tone (1-2 sentences max). "
                        "NEVER use robotic sci-fi jargon like 'System functioning within normal parameters' or 'Arrays operating at stable load'."
                    )
                }
            ]
            for msg in messages[-8:]:
                role = "user" if msg.type == "human" else "assistant"
                llm_messages.append({"role": role, "content": msg.content})

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=llm_messages,
                temperature=0.7,
                max_tokens=150
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"SurveX compile_final_response LLM error: {e}")

    # Contextual offline fallback
    q = user_query.lower().strip()
    if "how are you" in q or "how r u" in q:
        return "I'm doing great, Surya! Thanks for asking. How can I help you today?"
    elif any(greet in q for greet in ["hello", "hi", "hey", "what's up", "sup"]):
        return "Hey Surya! I'm here and ready to help. What's on your mind?"
    elif any(word in q for word in ["time", "date"]):
        from datetime import datetime
        now = datetime.now()
        return f"It is currently {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}."
    else:
        return f"Got it, Surya. How can I assist you further?"
