import sqlite3

class SQLite:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = self._initialize_database()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_name)
        return conn

    def run_query(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.executescript(query, params)
        else:
            cursor.executescript(query)
        self.conn.commit()
        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()

