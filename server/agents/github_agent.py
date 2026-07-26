import os
import json
from langchain_core.messages import AIMessage
from tools.github_tool import query_github_api
from groq import Groq

# Load github agent prompt
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "github_agent.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    GITHUB_SYSTEM_PROMPT = f.read()

def run_github_agent(messages):
    # Extract user query to parse dynamic limit & requested GitHub resource
    user_query = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_query = msg.content
            break

    # Fetch live GitHub data powered by PAT token in .env
    github_output = query_github_api(user_query)
    
    if isinstance(github_output, dict):
        output_str = json.dumps(github_output, indent=2)
    else:
        output_str = str(github_output)

    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {"role": "system", "content": GITHUB_SYSTEM_PROMPT},
                {"role": "system", "content": f"GitHub PAT Tool API Results for authenticated account:\n{output_str}"}
            ]
            for msg in messages[-3:]:
                role = "user" if msg.type == "human" else "assistant"
                llm_messages.append({"role": role, "content": msg.content})
                
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=llm_messages,
                temperature=0.3
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"GitHub agent LLM error: {e}")

    return f"GitHub Agent output:\n{output_str}"
