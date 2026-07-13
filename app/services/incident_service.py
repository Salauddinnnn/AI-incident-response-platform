from database.db import get_db_connection


def create_incident(user_id, website_id, title, severity, ai_summary, auto_heal_report=None):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO incidents (
                    user_id,
                    website_id,
                    title,
                    severity,
                    ai_summary,
                    auto_heal_report
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (user_id, website_id, title, severity, ai_summary, auto_heal_report)
            )
            incident_id = cursor.fetchone()[0]
        conn.commit()
    return incident_id


def get_user_incidents(user_id, search=None, severity=None, status=None, website_id=None, limit=100):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT
                    i.id,
                    i.title,
                    i.severity,
                    i.status,
                    i.ai_summary,
                    i.auto_heal_report,
                    i.created_at,
                    w.name AS website_name,
                    w.url AS website_url,
                    i.website_id
                FROM incidents i
                JOIN websites w ON w.id = i.website_id
                WHERE i.user_id = %s
            """
            params = [user_id]

            if search:
                query += " AND i.title ILIKE %s"
                params.append(f"%{search}%")
            if severity and severity != "all":
                query += " AND i.severity = %s"
                params.append(severity)
            if status and status != "all":
                query += " AND i.status = %s"
                params.append(status)
            if website_id:
                query += " AND i.website_id = %s"
                params.append(website_id)

            query += " ORDER BY i.created_at DESC LIMIT %s"
            params.append(limit)

            cursor.execute(query, params)
            return cursor.fetchall()


def get_incident_by_id(incident_id, user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    i.id,
                    i.title,
                    i.severity,
                    i.status,
                    i.ai_summary,
                    i.auto_heal_report,
                    i.created_at,
                    w.name AS website_name,
                    w.url AS website_url,
                    i.website_id
                FROM incidents i
                JOIN websites w ON w.id = i.website_id
                WHERE i.id = %s AND i.user_id = %s
                """,
                (incident_id, user_id)
            )
            return cursor.fetchone()


def resolve_incident(incident_id, user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE incidents
                SET status = 'resolved'
                WHERE id = %s AND user_id = %s AND status = 'open'
                RETURNING id
                """,
                (incident_id, user_id)
            )
            result = cursor.fetchone()
        conn.commit()
    return result is not None


def resolve_open_incidents_for_website(website_id, user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE incidents
                SET status = 'resolved'
                WHERE website_id = %s AND user_id = %s AND status = 'open'
                RETURNING id
                """,
                (website_id, user_id)
            )
            resolved = cursor.fetchall()
        conn.commit()
    return len(resolved)


def has_open_incident_for_website(website_id, user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id FROM incidents
                WHERE website_id = %s AND user_id = %s AND status = 'open'
                LIMIT 1
                """,
                (website_id, user_id)
            )
            return cursor.fetchone() is not None


def get_incident_stats(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE status = 'open') AS open_count,
                    COUNT(*) FILTER (WHERE severity = 'critical') AS critical_count
                FROM incidents
                WHERE user_id = %s
                """,
                (user_id,)
            )
            return cursor.fetchone()


def format_incident_row(row):
    return {
        "id": row[0],
        "title": row[1],
        "severity": row[2],
        "status": row[3],
        "ai_summary": row[4],
        "auto_heal_report": row[5],
        "created_at": row[6].isoformat() if row[6] else None,
        "website_name": row[7],
        "website_url": row[8],
        "website_id": row[9]
    }