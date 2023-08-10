""" import python's sqlite to wrap it in a class """
import sqlite3

class SQLite:
    """ wrapper class to ease the use of db """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = self._initialize_database()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_name)
        return conn

    def run_query(self, query, params=None):
        """ wrapper for running query on table """
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        res = cursor.fetchall()
        return res

    def close_connection(self):
        """ close connection to db """
        self.conn.close()
