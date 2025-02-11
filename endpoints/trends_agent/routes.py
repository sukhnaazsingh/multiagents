from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from agents.trends.trends_agent import TrendsAgent

trends_bp = Blueprint("trend", __name__)
trends_agent = TrendsAgent()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@trends_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Trend Analysis Agent is active!"})


@trends_bp.route("/upload", methods=["POST"])
def upload_csv():
    """Allows users to upload a Google Trends CSV file for analysis."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save file to uploads directory
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Process the CSV file with the Trend Agent
    result = trends_agent.analyze_trends_from_csv(file_path)

    return jsonify(result)
