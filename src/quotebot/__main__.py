"""
Main Program that manages and Runs the Bot

@author Derek Garcia
"""
import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from bot.QuoteBot import QuoteBot
from db.Database import Database


def main():
    # Run Bot
    database = Database(os.getenv("DATABASE_PATH"))
    bot = QuoteBot(database, os.getenv("BLACKLIST"))
    bot.run(os.getenv("TOKEN"))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', help="Environment file with database connection details")
    args = parser.parse_args()

    if args.environment is None:
        load_dotenv()
    else:
        load_dotenv(dotenv_path=Path(args.environment))

    main()
