import os
from langchain_core.messages import AIMessage
from tools.memory_tool import search_semantic_memories, save_semantic_memory
from groq import Groq

# Load memory agent prompt
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "memory_agent.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    MEMORY_SYSTEM_PROMPT = f.read()

def run_memory_agent(messages):
    user_query = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_query = msg.content
            break
            
    # Search ChromaDB for relevant memory entries
    memories = search_semantic_memories(user_query, limit=2)
    mem_str = "\n".join([f"- {m}" for m in memories]) if memories else "No relevant memories indexed yet."
    
    # Save current query as a semantic index trace
    import uuid
    save_semantic_memory(user_query, str(uuid.uuid4()))
    
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {"role": "system", "content": MEMORY_SYSTEM_PROMPT},
                {"role": "system", "content": f"Semantic database results:\n{mem_str}"}
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
            print(f"Memory agent LLM error: {e}")
            
    # Mock text fallback
    return f"Semantic database query active. Recall results:\n{mem_str}"
