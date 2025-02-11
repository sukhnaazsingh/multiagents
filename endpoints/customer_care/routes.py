import json
import os
import uuid

from flask import Blueprint, request, jsonify
from agents.customer_care.customer_care_agent import CustomerCareAgent

customer_care_bp = Blueprint("customer_care", __name__)
customer_care_agent = CustomerCareAgent()

CHAT_FILE = "chat_history.json"

if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump({}, f)

def load_chats():
    """Lade den gespeicherten Chatverlauf aus der JSON-Datei"""
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

def save_chats(chats):
    """Speichere den Chatverlauf in die JSON-Datei"""
    with open(CHAT_FILE, "w") as f:
        json.dump(chats, f, indent=4)

@customer_care_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Customer Care Agent is active!"})

@customer_care_bp.route("/chat", methods=["POST"])
def chat():
    """Handles customer inquiries with memory and dynamic ID extraction."""
    data = request.json
    session_id = data.get("session_id") or str(uuid.uuid4())
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    chat_history_store = load_chats()

    if session_id not in chat_history_store:
        chat_history_store[session_id] = []

    chat_history_store[session_id].append({"session_id": session_id, "sender": "user", "content": user_message})

    response = customer_care_agent.handle_customer_request(user_message, chat_history_store[session_id])

    chat_history_store[session_id].append({"session_id": session_id, "sender": "assistant", "content": response["messages"][-1].content})

    save_chats(chat_history_store)

    return jsonify({"response": chat_history_store[session_id]})

