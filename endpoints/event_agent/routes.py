from flask import Blueprint, jsonify
from agents.event.event_agent import EventAgent

event_bp = Blueprint("event", __name__)
event_agent = EventAgent()

@event_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Event Agent is active!"})

@event_bp.route("/insights", methods=["GET"])
def get_event_stock_insights():
    """Runs the ambient agent automatically and returns event insights."""
    insights = event_agent.run_ambient_check()
    return jsonify(insights)
