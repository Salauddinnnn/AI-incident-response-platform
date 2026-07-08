from database.db import get_db_connection


def create_incident(title, severity, ai_summary):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents (title, severity, ai_summary)
        VALUES (?, ?, ?)
    """, (title, severity, ai_summary))

    conn.commit()
    conn.close()


def get_all_incidents():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, severity, status, ai_summary, created_at
        FROM incidents
        ORDER BY id DESC
    """)

    incidents = cursor.fetchall()
    conn.close()

    return incidents


def resolve_open_incidents():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE incidents
        SET status = 'resolved'
        WHERE status = 'open'
    """)

    conn.commit()
    conn.close()