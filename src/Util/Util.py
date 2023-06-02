"""
Utility programs for commands

@author Derek Garcia
"""
import json
import random
import re

global MAX_QUOTEE_CHAR, QUOTE_PATH
MAX_QUOTEE_CHAR = 30


def disp_format(quotee):
    """
    Converts the quotee to a display format
    :param quotee: name to be converted
    :return: display_name
    """
    # attempt to upper both first and last name
    try:
        first_name = quotee.split(" ")[0]
        last_name = quotee.split(" ")[1]

        return f"{first_name[0].upper() + first_name[1:].lower()} {last_name[0].upper() + last_name[1:].lower()}"

    # Else just upper first name
    except:
        return quotee[0].upper() + quotee[1:].lower()


def rand_quote(quote_list, quotee):
    """
    Gets a random quote form the given quotee

    :param quote_list: list of all people and their DemoQuotes
    :param quotee: quotee to search for
    :return: random quote if found, None otherwise
    """

    if quotee in quote_list:

        # Get person from QUOTES and random quote
        person = quote_list[quotee]
        i = random.randrange(0, len(person))
        return person[i]['quote']

    # If name not in QUOTES
    else:
        return None


def is_command(msg):
    """
    Checks if given message is a command prefix or not

    :param msg: message to check
    :return: true if command, false otherwise
    """

    # attempt get first char
    try:
        command = msg.split(" ")[0]

        # check if match command lists
        if command in ["!qadd", "!q", "!qall", "!qrand", "!qstat", "!qhelp", "!qkill"]:
            return True

        # else not a command
        return False

    except IndexError:
        return False


def is_quote(msg):
    """
    Determines if message is quote like

    :param msg: message to check
    :return: true if quote like, false otherwise
    """
    # parse content
    content = msg.replace("\n", " ").split('-')
    raw_quote = content[0].replace("“", "\"").replace("”", "\"").strip()

    # attempt to see if quotee attached
    try:
        content[1]
    except IndexError:
        return False

    # Search for DemoQuotes
    if re.search(r'"(.*?)"', raw_quote) is None:
        return False

    # is a quote
    return True


def add_quote(src_dir, quote_data, raw_msg):
    """
    Attempts to add a 'quote-like' message to the json file

    :param src_dir: source directory
    :param quote_data: quote data to add to
    :param raw_msg: raw discord message to parse
    :return: True if successful, false otherwise
    """
    # parse content
    content = raw_msg.content.replace("\n", " ").split('-')

    quotee = content[1].lower().strip()

    # Alert really long quotee
    if len(quotee) > MAX_QUOTEE_CHAR:
        return False

    raw_quote = content[0].replace("“", "\"").replace("”", "\"").strip()
    # get quote
    quote = re.search(r'"(.*?)"', raw_quote).group(1)

    # attempt parse context
    post_quote = r'(?<=\"\s).*'  # all text after '\"\s'
    pre_quote = r'.*(?=\s\")'  # all text before '\s\"'

    # check before
    before = ""
    if re.search(pre_quote, raw_quote) is not None:
        before = re.search(pre_quote, raw_quote).group(0)

    # check after
    after = ""
    if re.search(post_quote, raw_quote) is not None:
        after = re.search(post_quote, raw_quote).group(0)

    # build quote
    full_quote = f"{before} \"{quote}\" {after}".strip()

    quote_obj = {'quote': full_quote,
                 'contributor': str(raw_msg.author.name),
                 'timestamp': str(raw_msg.created_at)
                 }

    if quotee not in quote_data['DemoQuotes']:
        quote_data['DemoQuotes'][quotee] = []

    # Append and update count
    quote_data['DemoQuotes'][quotee].append(quote_obj)
    quote_data['num_quotes'] += 1

    with open(src_dir + "/DemoQuotes.json", "w") as json_file:
        json_file.write(json.dumps(quote_data, indent=4))

    return True


def similar_names(quotes, keywords):
    """
    Generates a string of similar names in correct display format

    :param quotes: list of names in the database
    :param keywords: keywords to search for
    """
    # Find all matches
    suggest = ""
    for quotee in quotes:
        if keywords in quotee:
            suggest = f"{suggest}> {disp_format(quotee)}\n"

    # Return results
    if suggest == "":
        return None
    else:
        return suggest
