import sqlite3
import os

class JobDatabase:
    def __init__(self, db_name="jobs.db"):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(f"data/{db_name}")
        self.create_table()
    
    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    title TEXT,
                    company TEXT,
                    url TEXT,
                    platform TEXT,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def job_exists(self, job_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM jobs WHERE job_id = ?", (job_id,))
        return cursor.fetchone() is not None
    
    def add_job(self, job_id, title, company, url, platform):
        with self.conn:
            self.conn.execute(
                "INSERT INTO jobs (job_id, title, company, url, platform) VALUES (?, ?, ?, ?, ?)",
                (job_id, title, company, url, platform)
            )
    
    def close(self):
        self.conn.close()
