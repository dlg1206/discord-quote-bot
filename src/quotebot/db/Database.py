"""
File: Database.py
Description: Sqlite database interface for managing quotes

@author Derek Garcia
"""
import os
import sqlite3


class Database:
    def __init__(self, db_location: str, ddl_location: str):
        """
        Create new SQLite instance if it does not exist

        :param db_location: Location of the sqlite database
        :param ddl_location: Location of SQL files to init create the database
        """
        self.db_location = db_location
        self.ddl_location = ddl_location
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()

        # build db
        for file in os.scandir(self.ddl_location):
            # skip any non sql files
            if not (file.is_file() and file.name.endswith(".sql")):
                continue
            # Execute sql file
            with open(file, 'r') as sql_file:
                cur.executescript(sql_file.read())

        conn.commit()
        conn.close()


