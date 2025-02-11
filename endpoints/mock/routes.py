import datetime

from flask import Blueprint, request, jsonify
import random

mock_bp = Blueprint("mock", __name__)

@mock_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Mock event API is active!"})

# Predefined mock weather conditions
MOCK_WEATHER_DATA = {
    "New York": ["Sunny", "Cloudy", "Rainy", "Snowy", "Thunderstorms", "Foggy", "Windy"],
    "Los Angeles": ["Sunny", "Cloudy", "Foggy", "Windy", "Light Rain", "Very Hot"],
    "San Francisco": ["Foggy", "Cloudy", "Rainy", "Windy", "Cool", "Overcast"],
    "Miami": ["Hot", "Thunderstorms", "Partly Cloudy", "Humid", "Heavy Rain", "Hurricane Warning"],
    "Chicago": ["Windy", "Snowy", "Cloudy", "Thunderstorms", "Freezing Rain", "Icy Roads"],
    "Houston": ["Sunny", "Rainy", "Humid", "Storm Warning", "Flooding", "Hailstorm"],
    "Seattle": ["Rainy", "Overcast", "Drizzle", "Cold", "Stormy", "Gale Winds"],
    "Las Vegas": ["Hot", "Sunny", "Clear Night", "Sandstorm", "Extremely Dry"],
    "Denver": ["Snowy", "Clear", "Cloudy", "Freezing Fog", "Blizzard", "Cold Front"],
    "Boston": ["Rainy", "Snowy", "Cold", "Windy", "Nor'easter Warning", "Ice Storm"],
    "Atlanta": ["Cloudy", "Sunny", "Humid", "Foggy", "Heavy Rain", "Tornado Warning"],
    "Dallas": ["Windy", "Hot", "Cloudy", "Severe Storm", "Hail", "Flash Flood Warning"],
    "Philadelphia": ["Cold", "Windy", "Sunny", "Icy", "Snow Showers", "Black Ice Warning"],
    "Phoenix": ["Very Hot", "Sunny", "Dry", "Monsoon", "Dust Storm", "Extreme UV"],
    "San Diego": ["Mild", "Partly Cloudy", "Breezy", "Light Rain", "Cool"],
    "Detroit": ["Snow", "Ice", "Cloudy", "Cold", "Windy", "Fog"],
    "Minneapolis": ["Blizzard", "Freezing Rain", "Heavy Snow", "Icy Roads"],
    "St. Louis": ["Thunderstorms", "Heavy Rain", "Tornado Watch"],
    "Orlando": ["Hurricane Watch", "Hot", "Rainy", "Lightning Storms"],
    "Austin": ["Hot", "Humid", "Thunderstorms", "Storm Warnings"],
    "Portland": ["Rainy", "Cold", "Windy", "Stormy", "Fog"],
    "Las Cruces": ["Dust Storm", "Hot", "Dry"],
    "Salt Lake City": ["Snow", "Cold", "Windy", "Foggy"],
    "Kansas City": ["Tornado Warning", "Thunderstorms", "Hail"],
    "Baltimore": ["Rainy", "Cloudy", "Foggy", "Stormy"],
    "Charlotte": ["Foggy", "Humid", "Thunderstorms"],
    "Cleveland": ["Snow", "Icy Roads", "Windy"],
    "Pittsburgh": ["Cold", "Rainy", "Snow Showers"],
    "New Orleans": ["Hurricane Alert", "Humid", "Heavy Rain"],
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
    "New York": ["Music Festival", "Tech Conference", "Broadway Show", "Marathon", "Political Protest"],
    "Los Angeles": ["Film Premiere", "Hollywood Tour", "Food Festival", "Celebrity Event", "Red Carpet Closure"],
    "San Francisco": ["Tech Expo", "Art Exhibition", "Startup Pitch Night", "Pride Parade", "Street Closure"],
    "Miami": ["Beach Party", "Boat Show", "Carnival Parade", "Spring Break Crowds", "Hurricane Evacuation"],
    "Chicago": ["Jazz Concert", "Sports Game", "Food Market", "Winter Storm Warning", "Railway Strike"],
    "Houston": ["Rodeo Festival", "Space Exploration Fair", "Comic Con", "Flooding Alert", "Highway Closure"],
    "Seattle": ["Music Festival", "Startup Fair", "Wine Tasting Event", "Traffic Congestion Due to Bridge Closure"],
    "Las Vegas": ["Casino Gala", "Magic Show", "Auto Show", "Massive Convention", "High Tourist Activity"],
    "Denver": ["Hiking Meetup", "Beer Festival", "Ski Competition", "Snowstorm", "Mountain Road Closure"],
    "Boston": ["Marathon", "Harvard Lecture", "Cultural Night", "Blizzard Alert", "Ice Road Hazard"],
    "Atlanta": ["Rap Concert", "Film Festival", "Fashion Week", "Tornado Watch", "Traffic Jam Due to Stadium Event"],
    "Dallas": ["State Fair", "Business Summit", "Livestock Show", "Thunderstorm", "Airport Delays"],
    "Philadelphia": ["Historical Tour", "Orchestra Performance", "Food Truck Rally", "Snowstorm", "Protest Activity"],
    "Phoenix": ["Desert Racing", "Tattoo Convention", "Rock Concert", "Heatwave Alert", "Monsoon Season"],
    "San Diego": ["Comic Con", "Marine Corps Graduation", "Car Show", "Extreme Surf Conditions"],
    "Detroit": ["Auto Show", "Music Festival", "Sports Event", "Heavy Snowstorm"],
    "Minneapolis": ["Winter Festival", "Outdoor Ice Skating Championship", "Blizzard Warning"],
    "St. Louis": ["Baseball Game", "Food Festival", "Thunderstorm Alert"],
    "Orlando": ["Disney World Special Event", "Spring Break Crowds", "Hurricane Warning"],
    "Austin": ["SXSW Festival", "Music Festival", "Major Traffic Delays"],
    "Portland": ["Biking Marathon", "Rainy Season Street Closures"],
    "Las Cruces": ["Dust Storm Event", "Hot Air Balloon Show"],
    "Salt Lake City": ["Ski Championship", "Cold Weather Traffic Delays"],
    "Kansas City": ["Football Game", "State Fair", "Tornado Warning"],
    "Baltimore": ["Marathon", "Street Festival", "Harbor Traffic"],
    "Charlotte": ["Basketball Game", "Thunderstorm Alert"],
    "Cleveland": ["Baseball Game", "Concert Traffic"],
    "Pittsburgh": ["Football Match", "Heavy Snow"],
    "New Orleans": ["Mardi Gras Parade", "Jazz Festival", "Flooding Risk"],
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
