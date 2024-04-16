"""
Utility programs for commands

@author Derek Garcia
"""
import re

MAX_QUOTEE_CHAR = 30


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


def add_quote(database, raw_msg):
    """
    Attempts to add a 'quote-like' message to the json file

    :param database: database to upload quotes to
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

    return database.add_quote(full_quote, quotee, str(raw_msg.author.name)) == 0
