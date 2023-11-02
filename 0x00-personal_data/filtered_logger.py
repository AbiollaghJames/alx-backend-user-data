#!/usr/bin/env python3
"""
Regex-ing module
"""
import re
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
            f'{field}=(.*?){separator}',
            f'{field}={redaction}{separator}', message)
        return message
