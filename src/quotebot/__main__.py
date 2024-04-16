"""
Main Program that manages and Runs the Bot

@author Derek Garcia
"""
import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from bot.QuoteBot import QuoteBot
from util.Logger import init_log

global DEFAULT_QUOTE_FILE, LOG_PATH, LOG_FILE
DEFAULT_QUOTE_FILE = "quotes.json"


def load_quote_data(quotes_path):

    # Attempt to read data
    try:
        with open(quotes_path) as json_file:
            quotes = json.load(json_file)

        # Make sure quote count correct
        num_quotes = 0
        for quotee in quotes['quotes']:
            num_quotes += len(quotes['quotes'][quotee])

        # Quotes are correct
        if num_quotes == quotes['num_quotes']:
            print("count and stored match")
        # Update and fix count
        else:
            print("count and stored mismatched, updating ...")
            quotes['num_quotes'] = num_quotes

            with open(quotes_path, "w") as json_file:
                json_file.write(json.dumps(quotes, indent=4))

    except FileNotFoundError:
        print(f"File \'{quotes_path}\' was not found")
        print(f"Creating new file. . .")
        quotes = {"num_quotes": 0, "quotes": {}}
        with open(quotes_path, "w") as f:
            f.write(json.dumps(quotes, indent=4))
        return quotes
    except:
        print(f"Failed to parse file \'{quotes_path}\'")
        exit()

    return quotes


def main(token, quotes_path=None):

    # Attempt to load data if path given
    if quotes_path is not None:
        quotes = load_quote_data(quotes_path)
    else:
        global DEFAULT_QUOTE_FILE
        quotes_path = DEFAULT_QUOTE_FILE
        quotes = load_quote_data(DEFAULT_QUOTE_FILE)


    init_log()
    print("Data loaded, Bot is starting . . .")

    # Run Bot
    bot = QuoteBot(quotes, quotes_path)
    bot.run(token)
    print("done")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--environment', help="Environment file with database connection details")
    args = parser.parse_args()

    if args.environment is None:
        load_dotenv()
    else:
        load_dotenv(dotenv_path=Path(args.environment))

    main(os.getenv("TOKEN"))
