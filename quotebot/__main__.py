"""
File: __main.py__
Description: Main Program that loads env vars and launches bot

@author Derek Garcia
"""
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from Database import Database
from QuoteBot import QuoteBot


def main() -> None:
    """
    Init quote database and launch bot
    """
    database = Database(os.getenv("DATABASE_PATH"))
    bot = QuoteBot(database, os.getenv("BLACKLIST"))
    bot.run(os.getenv("TOKEN"))


if __name__ == '__main__':
    """
    Load env variables for bot to use
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', help="Environment file with database connection details")
    args = parser.parse_args()

    if args.environment is None:
        load_dotenv()
    else:
        load_dotenv(dotenv_path=Path(args.environment))

    try:
        assert os.getenv("TOKEN") is not None
        main()
    except AssertionError as ae:
        print("Missing Discord Token; Ensure the token environment variable has been defined in the env file",
              file=sys.stderr)
        exit(1)
