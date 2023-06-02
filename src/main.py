"""
Main Program that manages and Runs the Bot

@author Derek Garcia
"""

import json
import sys
from QuoteBot import start_bot
from Util.Logger import init_log


def load_quote_data(quotes_path):

    # Attempt to read data
    try:
        with open(quotes_path, "w") as json_file:
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
                json_file.write(json.dumps(quotes, indent=4))

    except FileNotFoundError:
        print(f"File \'{quotes_path}\' was not found")
        exit()
    except:
        print(f"Failed to parse file \'{quotes_path}\'")
        exit()

    return quotes


def main(quotes_path=None):

    # Attempt to load data if path given
    if quotes_path is not None:
        quotes = load_quote_data(quotes_path)
    else:
        quotes = {"num_quotes": 0, "quotes": {}}    # default

    # init_log(quotes_path)
    print("Data loaded, Bot is starting . . .")

    # Run Bot
    start_bot(quotes, quotes_path)
    print("done")


if __name__ == '__main__':

    if len(sys.argv) != 1:
        main(sys.argv[1])
    else:
        main()
