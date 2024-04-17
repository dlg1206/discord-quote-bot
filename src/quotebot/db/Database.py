"""
File: Database.py
Description: Sqlite database interface for managing quotes

@author Derek Garcia
"""
import os
import random
import sqlite3
from contextlib import contextmanager

from log.Logger import Status, Logger
from quote.Quote import Quote

DEFAULT_DB_PATH = "data/db/quotes.db"
DEFAULT_DDL_PATH = "data/ddl"


class Database:
    def __init__(self, db_location: str = DEFAULT_DB_PATH):
        """
        Create new SQLite instance if it does not exist

        :param db_location: Location of the sqlite database
        """
        # use defaults if empty or none
        self.db_location = DEFAULT_DB_PATH if db_location is None or not db_location else db_location
        self.ddl_location = DEFAULT_DDL_PATH

        # build db
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:

                for file in os.scandir(self.ddl_location):
                    # skip any non sql files
                    if not (file.is_file() and file.name.endswith(".sql")):
                        continue
                    # Execute sql file
                    with open(file, 'r') as sql_file:
                        cur.executescript(sql_file.read())

        self.logger = Logger(self)

    @contextmanager
    def open_connection(self) -> sqlite3.Connection:
        """
        Open a connection that can be closed on exit

        :return: Database connection
        """
        try:
            conn = sqlite3.connect(self.db_location)
            yield conn
        finally:
            conn.commit()
            conn.close()

    @contextmanager
    def get_cursor(self, connection: sqlite3.Connection) -> sqlite3.Cursor:
        """
        Open a cursor that can be closed on exit

        :param connection: Database connection to get the cursor for
        :return: cursor
        """
        try:
            cur = connection.cursor()
            yield cur
        finally:
            cur.close()

    def add_quote(self, quote: Quote, contributor: str) -> int:
        """
        Add a quote to the database

        :param quote: Quote to add
        :param contributor: Contributor who added the quote
        :return: Quote ID in database
        """
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:
                # Add new quotee if does not exist
                try:
                    cur.execute("INSERT INTO quotee VALUES (?);", (quote.quotee,))
                    conn.commit()
                except sqlite3.IntegrityError as ie:
                    conn.commit()
                    self.logger.log("database", "add quotee", Status.WARN, f'{str(ie)} "{quote.quotee}"')

                # Add new contributor if does not exist
                try:
                    cur.execute("INSERT INTO contributor VALUES (?);", (contributor,))
                    conn.commit()
                except sqlite3.IntegrityError as ie:
                    conn.commit()
                    self.logger.log("database", "add contributor", Status.WARN, f'{str(ie)} "{contributor}"')

                # Upload quote
                cur.execute(
                    "INSERT INTO quote (pre_context, quote, post_context, quotee, contributor) VALUES (?, ?, ?, ?, ?);",
                    (quote.pre_context, quote.quote, quote.post_context, quote.quotee, contributor)
                )
                conn.commit()

                # Get new ID
                cur.execute("SELECT MAX(ROWID) FROM quote")
                return cur.fetchall()[0][0]

    def find_similar_quotee(self, quotee: str) -> list[str]:
        """
        Get list of quotees that a similar to the given quotee

        :param quotee: Quotee to attempt to match
        :return: List of similar quotees
        """
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:
                # Find similar quotees
                cur.execute("SELECT name FROM quotee WHERE name LIKE ?;", (f"%{quotee}%",))
                data = cur.fetchall()
                conn.commit()
                return [q[0] for q in data]  # convert list of tuples for list of strings

    def get_all_quotees(self) -> list[str]:
        """
        Get all quotees in the database

        :return: List of quotees
        """
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:
                # Get all quotees
                cur.execute("SELECT name FROM quotee;")
                data = cur.fetchall()
                conn.commit()
                return [q[0] for q in data]  # convert list of tuples for list of strings

    def get_all_quotes(self, quotee: str = None) -> list[Quote]:
        """
        Get all quotes in database or for specific quotee

        :param quotee: Optional quotee to get all quotes for
        :return: List of Quotes
        """
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:

                # No quotee, get all quotes
                if quotee is None:
                    cur.execute("SELECT quote, quotee, pre_context, post_context FROM quote;")
                # Else get all quotes by person
                else:
                    cur.execute(
                        "SELECT quote, quotee, pre_context, post_context FROM quote WHERE quotee = ?;",
                        (quotee,)
                    )
                data = cur.fetchall()
                return [Quote(q[0], q[1], q[2], q[3]) for q in data]  # convert list of tuples for list of Quotes

    def get_rand_quote(self, quotee: str = None) -> Quote | None:
        """
        Get a random quote from entire database or specific quotee

        :param quotee: Optional quotee to get a random quote from
        :return: Quote or None if no quotes from quotee
        """
        quotes = self.get_all_quotes(quotee)
        if len(quotes) == 0:
            return None  # no quotes found
        # return random quote
        rand_id = random.randint(1, len(quotes))
        return quotes[rand_id]

    def get_quote_total(self, quotee: str = None) -> int:
        """
        Get the total number of quotes in the database or for a quotee

        :param quotee: Optional quotee to get a total quotes from
        :return: Number of quotes
        """
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:
                # Not quotee, get all quotes
                if quotee is None:
                    cur.execute("SELECT COUNT(ROWID) FROM quote;")
                # Else get count for specific quotee
                else:
                    cur.execute("SELECT COUNT(ROWID) FROM quote WHERE quotee = ?;", (quotee,))
                count = cur.fetchall()[0][0]
                return count

    def get_quotee_total(self) -> int:
        """
        Get the total number of quotees in the database

        :return: Number of quotees in the database
        """
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:
                cur.execute("SELECT COUNT(*) FROM quotee;")
                count = cur.fetchall()[0][0]
                return count

    def log(self, user: str, action: str, status: str, add_info=None) -> None:
        """
        Save log message to database

        :param user: User who performed the action
        :param action: Action perfomred
        :param status: Status / result of action
        :param add_info: Optional additional details to add
        """
        with self.open_connection() as conn:
            with self.get_cursor(conn) as cur:
                cur.execute(
                    "INSERT INTO log (user, action, status, additional_info) VALUES (?, ?, ?, ?);",
                    (user, action, status, add_info)
                )
