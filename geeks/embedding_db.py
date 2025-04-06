import sqlite3

class MemoryDB:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS outputs (
                agent TEXT,
                task TEXT,
                response TEXT
            )
        """)
        self.conn.commit()

    def store(self, agent, task, response):
        self.conn.execute("INSERT INTO outputs VALUES (?, ?, ?)", (agent, task, response))
        self.conn.commit()

    def fetch_all(self):
        return self.conn.execute("SELECT * FROM outputs").fetchall()
