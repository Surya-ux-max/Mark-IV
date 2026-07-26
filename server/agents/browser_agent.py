import os
import asyncio
from langchain_core.messages import AIMessage
from tools.search_tool import search_tavily
from groq import Groq

# Load browser agent prompt
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "browser_agent.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    BROWSER_SYSTEM_PROMPT = f.read()

def run_browser_agent(messages):
    # Retrieve user search query
    user_query = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_query = msg.content
            break
            
    # Fetch web results using Tavily Search Tool
    search_results = search_tavily(user_query)
    
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {"role": "system", "content": BROWSER_SYSTEM_PROMPT},
                {"role": "system", "content": f"Browser Search Results:\n{search_results[:1000]}"}
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
            print(f"Browser agent LLM error: {e}")
            
    # Mock text fallback
    return f"Web search completed for: {user_query}. Results index synced."
