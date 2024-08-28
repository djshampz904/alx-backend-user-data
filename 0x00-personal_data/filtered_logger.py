#!/usr/bin/env python3
"""Regex-ing returning log messages obfuscation and database connection"""
import re
from typing import List
import logging
import mysql.connector
import os

# PII fields to be redacted
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, rf"\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            log_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the MySQL database"""
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connection


def main() -> None:
    """Retrieve and display all rows in
    the users table under a filtered format"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        message = '; '.join(f"{k}={v}" for k, v in row.items())
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
