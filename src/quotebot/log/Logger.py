"""
Logger for actions

@author Derek Garcia
"""

import time
import json
from datetime import datetime
from enum import Enum

from db import Database

CLEAR = "\033[00m"


class Status(Enum):
    INFO = "",
    SUCCESS = "\033[92m",
    WARN = "\033[93m",
    ERROR = "\033[91m",

    def __str__(self):
        return f"{self.value[0]}{self.name}{CLEAR}"


class Logger:
    def __init__(self, database: Database):
        self.database = database

    def log(self, user: str, action: str, status: Status, add_info=None) -> None:
        # skip info details
        if status != Status.INFO:
            self.database.log(user, action, status.name, add_info)

        log_msg = f"{datetime.now()} | {status} | {user} | {action}"

        # add add. info if provided
        if add_info is not None:
            log_msg += f" | {add_info}"

        print(log_msg)
