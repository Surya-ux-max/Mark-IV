from database.db import get_all_calendar_events, save_calendar_event

def add_event(title: str, description: str, start_time: str, end_time: str) -> str:
    """Adds a calendar event entry to the built-in database scheduler."""
    try:
        save_calendar_event(title, description, start_time, end_time)
        return f"Calendar Tool: Event '{title}' scheduled successfully from {start_time} to {end_time}."
    except Exception as e:
        return f"Calendar Tool Error: Failed to schedule event: {e}"

def get_events() -> list:
    """Lists all upcoming calendar events in chronological order."""
    try:
        return get_all_calendar_events()
    except Exception as e:
        return [f"Calendar Tool Error: Failed to read events: {e}"]
