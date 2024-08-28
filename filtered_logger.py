#!/usr/bin/env python3
"""Regex-ing returning log messages obfuscation"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, rf"\1={redaction}", message)
