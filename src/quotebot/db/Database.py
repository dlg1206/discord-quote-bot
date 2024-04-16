"""
File: Database.py
Description: Sqlite database interface for managing quotes

@author Derek Garcia
"""
import os
import random
import sqlite3

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
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()

        for file in os.scandir(self.ddl_location):
            # skip any non sql files
            if not (file.is_file() and file.name.endswith(".sql")):
                continue
            # Execute sql file
            with open(file, 'r') as sql_file:
                cur.executescript(sql_file.read())

        conn.commit()
        conn.close()

    def add_quote(self, quote: Quote, contributor: str) -> int:
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO quotee VALUES (?);", (quote.quotee,))
            conn.commit()
        except sqlite3.IntegrityError as ie:
            # TODO log repeat
            print(ie)
        except Exception as e:
            # TODO log err
            print(e)
            conn.commit()
            conn.close()
            return 1

        try:
            cur.execute("INSERT INTO contributor VALUES (?);", (contributor,))
            conn.commit()
        except sqlite3.IntegrityError as ie:
            # TODO log repeat
            print(ie)
        except Exception as e:
            # TODO log err
            conn.commit()
            conn.close()
            return 2

        try:
            cur.execute(
                "INSERT INTO quote (pre_context, quote, post_context, quotee, contributor) VALUES (?, ?, ?, ?, ?);",
                (quote.pre_context, quote.quote, quote.post_context, quote.quotee, contributor)
            )
            conn.commit()
        except Exception as e:
            print(e)
            conn.commit()
            conn.close()
            return 3

        conn.commit()
        conn.close()
        return 0

    def find_similar_quotee(self, quotee: str) -> list[str]:
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()
        try:
            # Find similar quotees
            cur.execute("SELECT name FROM quotee WHERE name LIKE ?;", (f"%{quotee}%",))
            data = cur.fetchall()
            conn.commit()
            return [q[0] for q in data]

        except Exception as e:
            # TODO log err
            print(e)
            return []
        finally:
            conn.commit()
            conn.close()

    def get_all_quotees(self) -> list[str]:
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()
        try:
            # Get names
            cur.execute("SELECT name FROM quotee;")
            data = cur.fetchall()
            conn.commit()
            # format quotees
            return [q[0] for q in data]
        except Exception as e:
            # TODO log err
            print(e)
            return []
        finally:
            conn.commit()
            conn.close()

    def get_all_quotes(self, quotee: str = None) -> list[Quote]:
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()
        try:
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
            conn.commit()

            return [Quote(q[0], q[1], q[2], q[3]) for q in data]
        except Exception as e:
            # TODO log err
            print(e)
            return []
        finally:
            conn.commit()
            conn.close()

    def get_rand_quote(self, quotee: str = None) -> Quote | None:
        quotes = self.get_all_quotes(quotee)
        if len(quotes) == 0:
            return None
        rand_id = random.randint(1, len(quotes))
        return quotes[rand_id]

    def get_quote_total(self, quotee: str = None) -> int:
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()
        try:
            if quotee is None:
                cur.execute("SELECT COUNT(ROWID) FROM quote;")
            else:
                cur.execute("SELECT COUNT(ROWID) FROM quote WHERE quotee = ?;", (quotee,))
            count = cur.fetchall()[0][0]
            return count
        except Exception as e:
            # TODO log err
            print(e)
            return -1
        finally:
            conn.commit()
            conn.close()

    def get_quotee_total(self) -> int:
        conn = sqlite3.connect(self.db_location)
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM quotee;")
            count = cur.fetchall()[0][0]
            return count
        except Exception as e:
            # TODO log err
            print(e)
            return -1
        finally:
            conn.commit()
            conn.close()


if __name__ == '__main__':
    db = Database()
    # db.add_quote("foobar", "foo", "bar")
    # db.add_quote("foobar", "bar", "foo")
    # db.add_quote("foobar", "foo", "bar")
    # db.get_quote_total()
    # al = db.get_all_quotes()
    # foo = db.get_quote_total("b")
    # print(foo)
