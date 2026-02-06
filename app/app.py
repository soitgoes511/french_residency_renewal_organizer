"""
Flask application for French Residence Permit Renewal Tracker.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

from database import (
    init_db,
    get_permit_types,
    get_documents_with_status,
    mark_document_complete,
    mark_document_incomplete,
    update_document_notes,
    get_progress,
    reset_progress,
)
from documents import CATEGORIES, IMPORTANT_LINKS

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


@app.route("/api/documents/<permit_type>", methods=["GET"])
def api_get_documents(permit_type):
    """Get all documents for a permit type with status."""
    try:
        documents = get_documents_with_status(permit_type)
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


@app.route("/api/progress/<permit_type>", methods=["GET"])
def api_get_progress(permit_type):
    """Get progress for a permit type."""
    try:
        progress = get_progress(permit_type)
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
    return jsonify({"success": True, "data": CATEGORIES})


@app.route("/api/important-links", methods=["GET"])
def api_get_important_links():
    """Get important links for the application process."""
    return jsonify({"success": True, "data": IMPORTANT_LINKS})


if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("/app/data", exist_ok=True)

    # Initialize database
    init_db()

    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=False)
