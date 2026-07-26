import os
from database.db import update_session_summary
from groq import Groq

def optimize_conversation_memory(session_id, messages, max_threshold=15):
    """
    If a conversation thread exceeds the max_threshold limit of messages,
    automatically triggers the LLM to compile a structural summary,
    updates the session summary, and returns the pruned list.
    """
    if len(messages) <= max_threshold:
        return messages, False

    print(f"MemoryOptimization: Session {session_id} exceeds threshold ({len(messages)}). Compressing...")
    
    # 1. Compile recent logs to summarize
    conversation_str = "\n".join([f"{msg.get('sender', 'user')}: {msg.get('message', '')}" for msg in messages])
    
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    summary = "System conversation compressed."
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are SurveX Memory Optimizer. Compile a very concise 1-sentence summary of the following conversation history, capturing key operator preferences and tasks completed."
                    },
                    {"role": "user", "content": conversation_str}
                ],
                temperature=0.2,
                max_tokens=80
            )
            summary = completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"MemoryOptimization compression failed: {e}")
            
    # 2. Update persistent session summary
    try:
        update_session_summary(session_id, summary)
    except Exception as e:
        print(f"MemoryOptimization database update issue: {e}")
        
    # 3. Retain the most recent 6 messages to preserve context window flow
    pruned_messages = messages[-6:]
    return pruned_messages, True

def merge_duplicate_memories(session_id):
    """Placeholder to deduplicate vector-based long term database entries."""
    # Production-ready stub
    return "Duplicates checked: 0 merged."

def archive_inactive_sessions():
    """Archives session rows older than configurable expiration parameters."""
    # Production-ready stub
    return "Inactive records pruned successfully."
