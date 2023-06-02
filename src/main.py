"""
Main Program that manages and Runs the Bot

@author Derek Garcia
"""

import json
import sys
from QuoteBot import start_bot
from Util.Logger import init_log


def main(src_dir):
    # load file
    try:
        with open(src_dir + "\quotes.json") as json_file:
            quotes = json.load(json_file)
    except:
        print(f"Directory \'{src_dir}\' was not found")
        exit()
    # Make sure quote count correct
    num_quotes = 0
    for quotee in quotes['quotes']:
        num_quotes += len(quotes['quotes'][quotee])

    if num_quotes == quotes['num_quotes']:
        print("count and stored match")
    else:
        print("count and stored mismatched, updating ...")
        quotes['num_quotes'] = num_quotes
        with open(src_dir + "/quotes.json", "w") as json_file:
            json_file.write(json.dumps(quotes, indent=4))

    init_log(src_dir)
    print("Data loaded, Bot is starting . . .")
    # Run Bot
    start_bot(quotes, src_dir)

    print("done")


if __name__ == '__main__':
    # Default to 'DemoQuotes' if directory is not given
    if len(sys.argv) != 1:
        main(sys.argv[1])
    else:
        main("quotes")


