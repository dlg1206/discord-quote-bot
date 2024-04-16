"""
File: Quote.py
Description: 

@author Derek Garcia
"""


class Quote:
    def __init__(self, quote: str, quotee: str):
        self.quote = quote
        self.quotee = quotee

    def __str__(self):
        return f'"{self.quote}" -{format_quotee(self.quotee)}'


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
