import sqlite3
import os
from config import DB_PATH


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            country TEXT,
            url TEXT,
            first_seen TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def is_new(job_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT 1 FROM seen_jobs WHERE job_id = ?", (job_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return not exists


def mark_seen(job: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO seen_jobs (job_id, title, company, country, url) "
        "VALUES (?, ?, ?, ?, ?)",
        (job["job_id"], job["title"], job["company"], job["country"], job["url"]),
    )
    conn.commit()
    conn.close()
