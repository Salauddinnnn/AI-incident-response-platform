import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing from .env")

    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS websites (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    slow_threshold REAL DEFAULT 2.0,
                    request_timeout INTEGER DEFAULT 10,
                    current_status TEXT DEFAULT 'unknown',
                    status_code INTEGER DEFAULT NULL,
                    response_time_seconds REAL DEFAULT NULL,
                    last_error TEXT DEFAULT NULL,
                    last_checked_at TIMESTAMP DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS incidents (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    website_id INTEGER NOT NULL REFERENCES websites(id) ON DELETE CASCADE,
                    title TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    status TEXT DEFAULT 'open',
                    ai_summary TEXT,
                    auto_heal_report TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Migration: Add user_id to incidents if missing
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='incidents' AND column_name='user_id'
            """)
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE incidents ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE CASCADE")

            # Migration: Add website_id to incidents if missing
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='incidents' AND column_name='website_id'
            """)
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE incidents ADD COLUMN website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE")

            # Migration: Add auto_heal_report to incidents if missing
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='incidents' AND column_name='auto_heal_report'
            """)
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE incidents ADD COLUMN auto_heal_report TEXT")

            # Migration: Add monitoring columns to websites if missing
            columns_to_add = {
                "slow_threshold": "REAL DEFAULT 2.0",
                "request_timeout": "INTEGER DEFAULT 10",
                "current_status": "TEXT DEFAULT 'unknown'",
                "status_code": "INTEGER DEFAULT NULL",
                "response_time_seconds": "REAL DEFAULT NULL",
                "last_error": "TEXT DEFAULT NULL",
                "last_checked_at": "TIMESTAMP DEFAULT NULL",
                "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            }
            for col_name, col_type in columns_to_add.items():
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name='websites' AND column_name=%s
                """, (col_name,))
                if not cursor.fetchone():
                    cursor.execute(f"ALTER TABLE websites ADD COLUMN {col_name} {col_type}")

        conn.commit()