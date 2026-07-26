import os
from langchain_core.messages import AIMessage
from tools.weather_tool import get_live_weather
from groq import Groq

# Load weather agent prompt
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "weather_agent.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    WEATHER_SYSTEM_PROMPT = f.read()

def run_weather_agent(messages):
    # Fetch live weather data
    weather_data = get_live_weather()
    weather_str = f"Temp: {weather_data['temperature']}, Wind: {weather_data['windspeed']}, Status: {weather_data['status']}"
    
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            llm_messages = [
                {"role": "system", "content": WEATHER_SYSTEM_PROMPT},
                {"role": "system", "content": f"Weather Tool outputs:\n{weather_str}"}
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
            print(f"Weather agent LLM error: {e}")
            
    # Mock text fallback
    return f"Radar scan active: {weather_str}"
