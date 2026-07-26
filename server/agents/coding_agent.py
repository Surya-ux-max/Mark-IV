import os
from langchain_core.messages import AIMessage
from tools.file_tool import list_workspace_files
from groq import Groq

# Load coding agent prompt
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "coding_agent.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    CODING_SYSTEM_PROMPT = f.read()

def run_coding_agent(messages):
    # Retrieve local workspace directory structures
    files = list_workspace_files("client/src")
    files_str = "\n".join([f"- {f['name']} ({f['type']})" for f in files[:8]])
    
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {"role": "system", "content": CODING_SYSTEM_PROMPT},
                {"role": "system", "content": f"Workspace client/src directory index:\n{files_str}"}
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
            print(f"Coding agent LLM error: {e}")
            
    # Mock text fallback
    return f"Workspace folders analyzed. Project modules detected in client/src:\n{files_str}"
