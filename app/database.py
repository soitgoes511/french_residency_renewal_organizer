"""
SQLite database operations for residence permit application tracker.
Enhanced with notes, due dates, and profile selection.
"""

import sqlite3
import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any

from config_loader import (
    get_documents_for_permit,
    get_all_permit_types,
    get_profiles,
    get_categories,
)

DATABASE_PATH = os.environ.get("DATABASE_PATH", "/app/data/residence.db")


def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema and seed data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS permit_types (
            id TEXT PRIMARY KEY,
            name_fr TEXT NOT NULL,
            name_en TEXT NOT NULL,
            description TEXT,
            official_url TEXT,
            cost INTEGER,
            last_verified TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            permit_type TEXT NOT NULL,
            name_fr TEXT NOT NULL,
            name_en TEXT NOT NULL,
            description TEXT,
            category TEXT,
            profiles TEXT,
            link TEXT,
            link_text TEXT,
            validity_days INTEGER,
            sort_order INTEGER,
            FOREIGN KEY (permit_type) REFERENCES permit_types(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,
            is_complete INTEGER DEFAULT 0,
            completed_at TEXT,
            notes TEXT,
            due_date TEXT,
            FOREIGN KEY (document_id) REFERENCES documents(id),
            UNIQUE(document_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            selected_profiles TEXT DEFAULT 'common',
            selected_permit_type TEXT
        )
    """)

    # Initialize user settings if not exists
    cursor.execute("""
        INSERT OR IGNORE INTO user_settings (id, selected_profiles)
        VALUES (1, 'common')
    """)

    # Seed permit types from YAML
    for permit in get_all_permit_types():
        cursor.execute(
            """
            INSERT OR REPLACE INTO permit_types 
            (id, name_fr, name_en, description, official_url, cost, last_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                permit.get("id"),
                permit.get("name_fr"),
                permit.get("name_en"),
                permit.get("description"),
                permit.get("official_url"),
                permit.get("cost"),
                permit.get("last_verified"),
            ),
        )

    # Seed documents for each permit type from YAML
    for permit_type in ["carte_resident", "titre_sejour"]:
        documents = get_documents_for_permit(permit_type)
        for order, doc in enumerate(documents):
            profiles_str = ",".join(doc.get("profiles", ["common"]))
            cursor.execute(
                """
                INSERT OR REPLACE INTO documents 
                (id, permit_type, name_fr, name_en, description, category, 
                 profiles, link, link_text, validity_days, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    doc.get("id"),
                    permit_type,
                    doc.get("name_fr"),
                    doc.get("name_en"),
                    doc.get("description"),
                    doc.get("category"),
                    profiles_str,
                    doc.get("link"),
                    doc.get("link_text"),
                    doc.get("validity_days"),
                    order,
                ),
            )

            # Initialize status for each document
            cursor.execute(
                """
                INSERT OR IGNORE INTO document_status (document_id, is_complete)
                VALUES (?, 0)
            """,
                (doc.get("id"),),
            )

    conn.commit()
    conn.close()


def get_permit_types() -> List[Dict[str, Any]]:
    """Get all available permit types."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM permit_types")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user_settings() -> Dict[str, Any]:
    """Get user settings including selected profiles."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_settings WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        settings = dict(row)
        # Convert comma-separated profiles to list
        profiles_str = settings.get("selected_profiles", "common")
        settings["selected_profiles"] = (
            profiles_str.split(",") if profiles_str else ["common"]
        )
        return settings
    return {"selected_profiles": ["common"], "selected_permit_type": None}


def update_user_profiles(profiles: List[str]) -> bool:
    """Update user's selected profiles."""
    conn = get_db_connection()
    cursor = conn.cursor()
    profiles_str = ",".join(profiles) if profiles else "common"
    cursor.execute(
        """
        UPDATE user_settings SET selected_profiles = ? WHERE id = 1
    """,
        (profiles_str,),
    )
    conn.commit()
    conn.close()
    return True


def get_documents_with_status(
    permit_type: str, selected_profiles: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """Get all documents for a permit type with their completion status."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build query with optional profile filtering
    query = """
        SELECT d.*, ds.is_complete, ds.completed_at, ds.notes, ds.due_date
        FROM documents d
        LEFT JOIN document_status ds ON d.id = ds.document_id
        WHERE d.permit_type = ?
    """

    cursor.execute(query, (permit_type,))
    rows = cursor.fetchall()
    conn.close()

    documents = [dict(row) for row in rows]

    # Filter by profiles if specified
    if selected_profiles:
        profiles_set = set(selected_profiles)
        profiles_set.add("common")  # Always include common

        filtered = []
        for doc in documents:
            doc_profiles = set(doc.get("profiles", "common").split(","))
            if doc_profiles & profiles_set:
                filtered.append(doc)
        documents = filtered

    # Sort by sort_order
    documents.sort(key=lambda x: x.get("sort_order", 0))

    # Convert profiles string to list
    for doc in documents:
        doc["profiles"] = doc.get("profiles", "common").split(",")

    return documents


def mark_document_complete(document_id: str) -> bool:
    """Mark a document as complete."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE document_status 
        SET is_complete = 1, completed_at = datetime('now')
        WHERE document_id = ?
    """,
        (document_id,),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def mark_document_incomplete(document_id: str) -> bool:
    """Mark a document as incomplete."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE document_status 
        SET is_complete = 0, completed_at = NULL
        WHERE document_id = ?
    """,
        (document_id,),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def update_document_notes(document_id: str, notes: str) -> bool:
    """Update notes for a document."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE document_status 
        SET notes = ?
        WHERE document_id = ?
    """,
        (notes, document_id),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def update_document_due_date(document_id: str, due_date: Optional[str]) -> bool:
    """Update due date for a document."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE document_status 
        SET due_date = ?
        WHERE document_id = ?
    """,
        (due_date, document_id),
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def get_progress(
    permit_type: str, selected_profiles: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Get completion progress for a permit type."""
    # Get filtered documents
    documents = get_documents_with_status(permit_type, selected_profiles)

    total = len(documents)
    completed = sum(1 for doc in documents if doc.get("is_complete"))

    percentage = (completed / total * 100) if total > 0 else 0
    return {
        "total": total,
        "completed": completed,
        "remaining": total - completed,
        "percentage": round(percentage, 1),
    }


def reset_progress(permit_type: str) -> bool:
    """Reset all progress for a permit type."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE document_status 
        SET is_complete = 0, completed_at = NULL, notes = NULL, due_date = NULL
        WHERE document_id IN (
            SELECT id FROM documents WHERE permit_type = ?
        )
    """,
        (permit_type,),
    )
    conn.commit()
    conn.close()
    return True


def get_available_profiles() -> Dict[str, Any]:
    """Get all available profiles from YAML config."""
    return get_profiles()


def get_available_categories() -> Dict[str, Any]:
    """Get all available categories from YAML config."""
    return get_categories()
