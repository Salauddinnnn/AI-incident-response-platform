from database.db import get_db_connection


def create_incident(title, severity, ai_summary):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO incidents (
                    title,
                    severity,
                    ai_summary
                )
                VALUES (%s, %s, %s)
                """,
                (title, severity, ai_summary)
            )

        conn.commit()


def get_all_incidents():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    severity,
                    status,
                    ai_summary,
                    created_at
                FROM incidents
                ORDER BY id DESC
                """
            )

            return cursor.fetchall()


def resolve_open_incidents():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE incidents
                SET status = 'resolved'
                WHERE status = 'open'
                """
            )

        conn.commit()