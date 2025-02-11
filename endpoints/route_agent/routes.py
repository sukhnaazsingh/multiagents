from flask import Blueprint, request, jsonify
from agents.route.route_agent import RouteAgent

route_bp = Blueprint("route", __name__)
route_agent = RouteAgent()

@route_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Route Agent is active!"})

@route_bp.route("/analyze", methods=["POST"])
def analyze_route():
    """Fetches weather, events, and gives route recommendations."""
    data = request.json
    start = data.get("start")
    end = data.get("end")

    if not start or not end:
        return jsonify({"error": "Missing required fields: 'start' and 'end'"}), 400

    response = route_agent.get_route_analysis(start, end)
    return jsonify(response)
