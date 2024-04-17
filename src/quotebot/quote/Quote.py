"""
File: Quote.py
Description: Util quote object to hold quote information

@author Derek Garcia
"""
import re

# Matches: (pre-context) "quote" (post-context) - quotee
QUOTE_REGEX = re.compile('(?:\\((.*)\\)|).*?\\"(.*)\"(?:.*?\\((.*)\\)|).*?-(.*)')


class Quote:
    def __init__(self, quote: str, quotee: str, pre_context: str = None, post_context: str = None):
        """
        Create a new Quote

        :param quote: Quote message
        :param quotee: Quotee
        :param pre_context: Optional pre context to quote
        :param post_context: Option post context to quote
        """
        self.pre_context = pre_context
        self.quote = quote.strip()
        self.post_context = post_context
        self.quotee = quotee.strip().lower()

    def __str__(self):
        """
        Pre and post only if present
        :return: (pre-context) "quote" (post-context) - quotee
        """
        pre_context = f"({self.pre_context}) " if self.pre_context is not None else ""
        post_context = f" ({self.post_context})" if self.post_context is not None else ""
        return f'{pre_context}"{self.quote}"{post_context} -{format_quotee(self.quotee)}'


def format_quotee(quotee: str) -> str:
    """
    Converts the quotee to a display format

    :return: Formatted quotee name
    """
    # attempt to upper both first and last name
    try:
        first_name = quotee.split(" ")[0]
        last_name = quotee.split(" ")[1]

        return f"{first_name[0].upper() + first_name[1:].lower()} {last_name[0].upper() + last_name[1:].lower()}"

    # Else just upper first name
    except Exception as e:
        return quotee[0].upper() + quotee[1:].lower()


def parse_quote(message: str) -> Quote:
    """
    Use regex to parse a message

    :param message: Message to parse
    :return: Quote object extracted from message
    """
    match = QUOTE_REGEX.match(message.strip())
    return Quote(
        pre_context=match.group(1),
        quote=match.group(2),
        post_context=match.group(3),
        quotee=match.group(4)
    )


def is_quote(message: str) -> bool:
    """
    Use regex to attempt to match

    :param message: Message to parse
    :return: True if match, false otherwise
    """
    return bool(re.search(QUOTE_REGEX, message.strip()))
