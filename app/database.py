"""
SQLite database operations for residence permit application tracker.
"""

import sqlite3
import os
from typing import Optional
from documents import get_documents_for_permit, PERMIT_TYPES

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
            official_url TEXT
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
            link TEXT,
            link_text TEXT,
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
            FOREIGN KEY (document_id) REFERENCES documents(id),
            UNIQUE(document_id)
        )
    """)

    # Seed permit types if not exist
    for permit_id, permit_data in PERMIT_TYPES.items():
        cursor.execute(
            """
            INSERT OR IGNORE INTO permit_types (id, name_fr, name_en, description, official_url)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                permit_data["id"],
                permit_data["name_fr"],
                permit_data["name_en"],
                permit_data["description"],
                permit_data["official_url"],
            ),
        )

    # Seed documents for each permit type
    for permit_type in PERMIT_TYPES.keys():
        documents = get_documents_for_permit(permit_type)
        for order, doc in enumerate(documents):
            cursor.execute(
                """
                INSERT OR IGNORE INTO documents 
                (id, permit_type, name_fr, name_en, description, category, link, link_text, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    doc["id"],
                    permit_type,
                    doc["name_fr"],
                    doc["name_en"],
                    doc["description"],
                    doc["category"],
                    doc["link"],
                    doc["link_text"],
                    order,
                ),
            )

            # Initialize status for each document
            cursor.execute(
                """
                INSERT OR IGNORE INTO document_status (document_id, is_complete)
                VALUES (?, 0)
            """,
                (doc["id"],),
            )

    conn.commit()
    conn.close()


def get_permit_types():
    """Get all available permit types."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM permit_types")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_documents_with_status(permit_type: str):
    """Get all documents for a permit type with their completion status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT d.*, ds.is_complete, ds.completed_at, ds.notes
        FROM documents d
        LEFT JOIN document_status ds ON d.id = ds.document_id
        WHERE d.permit_type = ?
        ORDER BY d.sort_order
    """,
        (permit_type,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


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


def get_progress(permit_type: str) -> dict:
    """Get completion progress for a permit type."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM documents d
        WHERE d.permit_type = ?
    """,
        (permit_type,),
    )
    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) as completed
        FROM documents d
        JOIN document_status ds ON d.id = ds.document_id
        WHERE d.permit_type = ? AND ds.is_complete = 1
    """,
        (permit_type,),
    )
    completed = cursor.fetchone()["completed"]

    conn.close()

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
        SET is_complete = 0, completed_at = NULL, notes = NULL
        WHERE document_id IN (
            SELECT id FROM documents WHERE permit_type = ?
        )
    """,
        (permit_type,),
    )
    conn.commit()
    conn.close()
    return True
