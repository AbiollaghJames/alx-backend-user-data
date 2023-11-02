#!/usr/bin/env python3
"""
Regex-ing module
"""
import re
import logging
from typing import List


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Function that returns the log
    message obfuscated, the function
    should use a regex to replace occurrences
    of certain field values
    """
    for field in fields:
        message = re.sub(
            f'{field}=.*?{separator}',
            f'{field}={redaction}{separator}', message)
        return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
         filter values in incoming log
         records using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)