import datetime

from flask import Blueprint, request, jsonify
import random

mock_bp = Blueprint("mock", __name__)

@mock_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Mock event API is active!"})

# Predefined mock weather conditions
MOCK_WEATHER_DATA = {
    "New York": ["Sunny", "Cloudy", "Rainy", "Snowy"],
    "Los Angeles": ["Sunny", "Cloudy", "Foggy"],
    "San Francisco": ["Foggy", "Cloudy", "Rainy"],
    "Miami": ["Hot", "Thunderstorms", "Partly Cloudy"],
    "Chicago": ["Windy", "Snowy", "Cloudy"],
    "Houston": ["Sunny", "Rainy", "Humid"],
    "Seattle": ["Rainy", "Overcast", "Drizzle"],
    "Las Vegas": ["Hot", "Sunny", "Clear Night"],
    "Denver": ["Snowy", "Clear", "Cloudy"],
    "Boston": ["Rainy", "Snowy", "Cold"],
    "Atlanta": ["Cloudy", "Sunny", "Humid"],
    "Dallas": ["Windy", "Hot", "Cloudy"],
    "Philadelphia": ["Cold", "Windy", "Sunny"],
    "Phoenix": ["Very Hot", "Sunny", "Dry"]
}

@mock_bp.route("/weather", methods=["GET"])
def get_mock_weather():
    """
    Returns mock weather for a given location.
    If the location is not found, it returns a random condition.
    """
    location = request.args.get("location", "").title()  # Normalize capitalization

    if not location:
        return jsonify({"error": "Missing required parameter: location"}), 400

    # Generate mock weather data
    conditions = MOCK_WEATHER_DATA.get(location, ["Unknown"])
    condition = random.choice(conditions)
    temperature = random.randint(-5, 40)  # Random temperature between -5°C and 40°C

    return jsonify({"location": location, "condition": condition, "temperature": temperature})

# Predefined mock events for different locations
MOCK_EVENTS = {
    "New York": ["Music Festival", "Tech Conference", "Broadway Show"],
    "Los Angeles": ["Film Premiere", "Hollywood Tour", "Food Festival"],
    "San Francisco": ["Tech Expo", "Art Exhibition", "Startup Pitch Night"],
    "Miami": ["Beach Party", "Boat Show", "Carnival Parade"],
    "Chicago": ["Jazz Concert", "Sports Game", "Food Market"],
    "Houston": ["Rodeo Festival", "Space Exploration Fair", "Comic Con"],
    "Seattle": ["Music Festival", "Startup Fair", "Wine Tasting Event"],
    "Las Vegas": ["Casino Gala", "Magic Show", "Auto Show"],
    "Denver": ["Hiking Meetup", "Beer Festival", "Ski Competition"],
    "Boston": ["Marathon", "Harvard Lecture", "Cultural Night"],
    "Atlanta": ["Rap Concert", "Film Festival", "Fashion Week"],
    "Dallas": ["State Fair", "Business Summit", "Livestock Show"],
    "Philadelphia": ["Historical Tour", "Orchestra Performance", "Food Truck Rally"],
    "Phoenix": ["Desert Racing", "Tattoo Convention", "Rock Concert"]
}

@mock_bp.route("/events", methods=["GET"])
def get_event_stock_insights():
    """
    Returns mock events for a given location and date.
    If no events are found for that location, an empty list is returned.
    """
    location = request.args.get("location", "").title()  # Normalize capitalization
    date = request.args.get("date", datetime.date.today().strftime('%Y-%m-%d'))

    if not location:
        return jsonify({"error": "Missing required parameter: location"}), 400

    # Simulate random event availability (50% chance of empty)
    events = MOCK_EVENTS.get(location, [])
    selected_events = random.sample(events, random.randint(0, min(3, len(events)))) if events else []

    return jsonify({"location": location, "date": date, "events": selected_events})
