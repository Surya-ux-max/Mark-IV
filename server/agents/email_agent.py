import os
from langchain_core.messages import AIMessage
from tools.email_tool import send_smtp_email
from groq import Groq

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "email_agent.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    EMAIL_SYSTEM_PROMPT = f.read()

def run_email_agent(messages):
    user_query = ""
    for msg in reversed(messages):
        if msg.type == "human":
            user_query = msg.content
            break
            
    # Parse destination address or draft content
    to_email = "suryapr.exe14@gmail.com" # Default operator email
    subject = "SurveX Operating System Notification"
    body_text = f"Hello Surya,\n\nThis is a notification from your SurveX OS platform supervisor.\nQuery: {user_query}"
    
    # Trigger SMTP email send
    result = send_smtp_email(to_email, subject, body_text)

    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {"role": "system", "content": EMAIL_SYSTEM_PROMPT},
                {"role": "system", "content": f"Email Tool outputs:\n{result}"}
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
            print(f"Email agent LLM error: {e}")
            
    return result
