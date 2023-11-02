#!/usr/bin/env python3
"""
Regex-ing module
"""
import re
import logging
import mysql.connector
from typing import List
from os import environ

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """
     returns a logging.Logger object
    """
    logger = logging.getLogger('user_data').setLevel(logging.INFO)
    logger.propagate = False

    s_handler = logging.StreamHandler()
    s_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(s_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
     returns a connector to the database
    """
    conn = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return conn


def main() -> None:
    """
    obtain a database connection using get_db and
    retrieve all rows in the users table and display
    each row under a filtered format like this
    """
    db_conn = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    h = [i[0] for i in cursor.description]
    logger = get_logger()

    for r in cursor:
        ans = ''
        for x, y in zip(r, h):
            ans += '{}={}'.format(y, x)
        logger.info(ans)
    
    cursor.close()
    db.close()


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
        record.message = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()