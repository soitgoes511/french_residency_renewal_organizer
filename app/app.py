"""
Flask application for French Residence Permit Renewal Tracker.
Enhanced with profile selection, notes, and due dates.
"""

import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from config_loader import get_categories, get_important_links, get_metadata
from database import (
    get_available_profiles,
    get_documents_with_status,
    get_permit_types,
    get_progress,
    get_user_settings,
    init_db,
    mark_document_complete,
    mark_document_incomplete,
    reset_progress,
    update_document_due_date,
    update_document_notes,
    update_user_profiles,
)

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)


@app.route("/")
def index():
    """Serve the main application page."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/permit-types", methods=["GET"])
def api_get_permit_types():
    """Get all available permit types."""
    try:
        permit_types = get_permit_types()
        return jsonify({"success": True, "data": permit_types})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/profiles", methods=["GET"])
def api_get_profiles():
    """Get all available applicant profiles."""
    try:
        profiles = get_available_profiles()
        return jsonify({"success": True, "data": profiles})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/user-settings", methods=["GET"])
def api_get_user_settings():
    """Get user's current settings."""
    try:
        settings = get_user_settings()
        return jsonify({"success": True, "data": settings})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/user-settings/profiles", methods=["POST"])
def api_update_user_profiles():
    """Update user's selected profiles."""
    try:
        data = request.get_json()
        profiles = data.get("profiles", ["common"])
        success = update_user_profiles(profiles)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/documents/<permit_type>", methods=["GET"])
def api_get_documents(permit_type):
    """Get all documents for a permit type with status, filtered by profiles."""
    try:
        # Get selected profiles from query param or user settings
        profiles_param = request.args.get("profiles")
        if profiles_param:
            selected_profiles = profiles_param.split(",")
        else:
            settings = get_user_settings()
            selected_profiles = settings.get("selected_profiles", ["common"])

        documents = get_documents_with_status(permit_type, selected_profiles)
        return jsonify({"success": True, "data": documents})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/documents/<document_id>/complete", methods=["POST"])
def api_complete_document(document_id):
    """Mark a document as complete."""
    try:
        success = mark_document_complete(document_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/documents/<document_id>/incomplete", methods=["POST"])
def api_incomplete_document(document_id):
    """Mark a document as incomplete."""
    try:
        success = mark_document_incomplete(document_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/documents/<document_id>/notes", methods=["POST"])
def api_update_notes(document_id):
    """Update notes for a document."""
    try:
        data = request.get_json()
        notes = data.get("notes", "")
        success = update_document_notes(document_id, notes)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/documents/<document_id>/due-date", methods=["POST"])
def api_update_due_date(document_id):
    """Update due date for a document."""
    try:
        data = request.get_json()
        due_date = data.get("due_date")  # Can be null to clear
        success = update_document_due_date(document_id, due_date)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/progress/<permit_type>", methods=["GET"])
def api_get_progress(permit_type):
    """Get progress for a permit type."""
    try:
        # Get selected profiles from query param or user settings
        profiles_param = request.args.get("profiles")
        if profiles_param:
            selected_profiles = profiles_param.split(",")
        else:
            settings = get_user_settings()
            selected_profiles = settings.get("selected_profiles", ["common"])

        progress = get_progress(permit_type, selected_profiles)
        return jsonify({"success": True, "data": progress})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/reset/<permit_type>", methods=["POST"])
def api_reset_progress(permit_type):
    """Reset all progress for a permit type."""
    try:
        success = reset_progress(permit_type)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/categories", methods=["GET"])
def api_get_categories():
    """Get category definitions."""
    try:
        categories = get_categories()
        return jsonify({"success": True, "data": categories})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/important-links", methods=["GET"])
def api_get_important_links():
    """Get important links for the application process."""
    return jsonify({"success": True, "data": get_important_links()})


@app.route("/api/metadata", methods=["GET"])
def api_get_metadata():
    """Get configuration metadata (last verified date, source)."""
    try:
        metadata = get_metadata()
        return jsonify({"success": True, "data": metadata})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("/app/data", exist_ok=True)

    # Initialize database
    init_db()

    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=False)
