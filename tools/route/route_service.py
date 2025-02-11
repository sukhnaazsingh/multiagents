import requests
import datetime
from langchain_core.tools import tool

MOCK_WEATHER_API_URL = "http://127.0.0.1:5000/mock/weather"

@tool
def get_weather(location: str) -> str:
    """
    Fetches mock weather conditions for a given location.

    :param location: City or place name.
    :return: Weather conditions in a structured format.
    """
    response = requests.get(f"{MOCK_WEATHER_API_URL}?location={location}")

    if response.status_code == 200:
        data = response.json()
        return f"{location}: {data['condition']}, {data['temperature']}°C"
    else:
        return f"Could not fetch weather for {location}."


MOCK_API_URL = "http://127.0.0.1:5000/mock/events"

@tool
def get_events_near_route(start: str, end: str) -> str:
    """
    Fetches mock events happening near the typical route between two locations.

    :param start: Starting location.
    :param end: Destination location.
    :return: A structured string containing events occurring near the route.
    """
    today = datetime.date.today().strftime('%Y-%m-%d')

    # Fetch events for start and end locations
    response_start = requests.get(f"{MOCK_API_URL}?location={start}&date={today}")
    response_end = requests.get(f"{MOCK_API_URL}?location={end}&date={today}")

    events = []

    if response_start.status_code == 200:
        data = response_start.json()
        if data["events"]:
            events.append(f"{start}: {', '.join(data['events'])}")

    if response_end.status_code == 200:
        data = response_end.json()
        if data["events"]:
            events.append(f"{end}: {', '.join(data['events'])}")

    # Generate output response
    if events:
        return f"Events near the route:\n" + "\n".join(events)
    else:
        return "No major events detected near the route."

@tool
def generate_recommendation(weather_start: str, weather_end: str, events: str) -> str:
    """
    Generates a travel recommendation based on weather conditions and events.

    :param weather_start: Weather conditions at the starting location.
    :param weather_end: Weather conditions at the destination.
    :param events: Events occurring along the route.
    :return: Travel recommendation message.
    """
    return f"""
    Based on the conditions:
    - Weather at Start: {weather_start}
    - Weather at End: {weather_end}
    - Events Near Route: {events}

    Recommended action:
    1. If weather is bad at either location, drive cautiously.
    2. If there are major events, expect congestion.
    3. If all conditions are clear, the route is good to go.
    """
