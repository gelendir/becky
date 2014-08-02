#!/usr/bin/env python
"""

Becky Spam Rate Limiter

A simple AGI script for preventing spammers and script kiddies
from making too many calls to becky. Limits the number of calls
per day (By default maximum is 5 calls). Records the caller's number
and counts the number of calls made.

"""
from sys import stdin, stdout
from datetime import datetime
import logging
import re
import sqlite3

ROOT = '/var/lib/asterisk/becky'
DB_FILEPATH = '{}/database/db.sqlite'.format(ROOT)
LOG_FILEPATH = '{}/logs/rate_limit.log'.format(ROOT)

RESPONSE_REGEX = re.compile(r"(\d+) result=(\d+) ?(.*)")
MAX_CALLS_PER_DAY = 5

database = sqlite3.connect(DB_FILEPATH)

def read_env_variables():
    variables = {}
    line = stdin.readline()

    while line != "\n":
        key, value = line.split(":", 1)
        variables[key] = value.strip()
        line = stdin.readline()

    return variables


def execute(command):
    logging.debug('executing command %s', command)
    stdout.write(command + '\n')
    stdout.flush()

    response = stdin.readline()
    logging.debug('response: %s', response)

    match = RESPONSE_REGEX.match(response)
    if not match:
        raise Exception("did not receive proper response: %s" % response)

    return match.group(1), match.group(2), match.group(3)


def get_phone_number():
    _, _, phone_number = execute("GET FULL VARIABLE ${CALLERID(num)}")
    return phone_number.strip('()')


def set_variable(name, value):
    execute('SET VARIABLE %s %s' % (name, value))


def add_call_to_db(phone_number):
    cursor = database.cursor()
    query = "INSERT INTO calls(number, started_at) VALUES (?, ?)"
    cursor.execute(query, (phone_number, datetime.now()))
    database.commit()


def calls_today(phone_number):
    now = datetime.now()
    today = datetime(now.year, now.month, now.day, 0, 0, 0)

    cursor = database.cursor()
    query = "SELECT COUNT(*) FROM calls WHERE started_at > ? AND number = ?"
    calcursor.execute(query, (today,phone_number))

    calls_made = cursor.fetchone()[0]
    logger.debug('calls made by %s: %s', number, calls_made)

    return calls_made


def main():
    logging.info('script started')
    env = read_env_variables()
    logging.info('asterisk env variables: %s', env)

    phone_number = get_phone_number()
    add_call_to_db(phone_number)
    allowed = calls_today(phone_number) <= MAX_CALLS_PER_DAY
    set_variable('caller_allowed', int(allowed))


if __name__ == "__main__":
    logging.basicConfig(filename=LOG_FILEPATH, level=logging.DEBUG)
    try:
        main()
    except Exception as e:
        logging.exception(str(e), exc_info=True)
