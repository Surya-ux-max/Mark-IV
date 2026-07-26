import requests

def get_live_weather(lat=13.0827, lon=80.2707):  # Default to Chennai coordinates
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json().get("current_weather", {})
            return {
                "temperature": f"{data.get('temperature', 21)}°C",
                "windspeed": f"{data.get('windspeed', 12)} km/h",
                "winddirection": data.get("winddirection", 0),
                "weathercode": data.get("weathercode", 0),
                "status": "SECURE BAROMETRIC GRADIENT"
            }
    except Exception as e:
        print(f"Weather API error: {e}")
    
    # Fallback mock weather data
    return {
        "temperature": "21°C",
        "windspeed": "10 km/h",
        "winddirection": 180,
        "weathercode": 0,
        "status": "SECURE BAROMETRIC GRADIENT"
    }
