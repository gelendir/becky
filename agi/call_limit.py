#!/usr/bin/env python
"""

Becky Call Limiter

An AGI script for preventing spammers and script kiddies from making too many
calls to becky. Limits the number of calls made by counting the following
conditions :

 - calls made by the same phone number
 - calls made inside the last minute
 - concurrent calls (i.e. number of people calling at the same time)

If one of these conditions exceeds the configured limits, then the call is
refused. Optionally, an email alert can also be sent. (deactivated by default)

default configuration parameters can be changed by creating a file 'config.ini'
and overriding their values.

"""
import os
import logging
import re
import sqlite3

from sys import stdin, stdout, argv
from datetime import datetime, timedelta
from ConfigParser import ConfigParser
from marrow.mailer import Mailer, Message


ROOT = os.path.dirname(os.path.abspath(__file__))

DB_FILEPATH = os.path.join(ROOT, 'database', 'db.sqlite')
LOG_FILEPATH = os.path.join(ROOT, 'logs', 'call_limit.log')
CONFIG_FILEPATHS = [os.path.join(ROOT, 'defaults.ini'),
                    os.path.join(ROOT, 'config.ini')]

LOG_FORMAT = "%(asctime)s %(levelname)s:%(name)s - %(message)s"
RESPONSE_REGEX = re.compile(r"(\d+) result=(\d+)( \((.*)\))?")
EMAIL_MESSAGE = """
Becky Spam alert !

number: {number}
calls made today : {calls_today}
calls made per minute : {calls_per_minute}
concurrent calls : {concurrent_calls}
"""

logger = logging.getLogger(__name__)
database = sqlite3.connect(DB_FILEPATH)

config = ConfigParser()
config.read(CONFIG_FILEPATHS)

def read_env_variables():
    variables = {}
    line = stdin.readline()

    while line != "\n":
        key, value = line.split(":", 1)
        variables[key] = value.strip()
        line = stdin.readline()

    return variables


def execute(command):
    logger.debug('command: %s', command)
    stdout.write(command + '\n')
    stdout.flush()

    response = stdin.readline()
    logger.debug('response: %s', response)

    match = RESPONSE_REGEX.match(response)
    if not match:
        raise Exception("unknown response format: %s" % response)

    return match.group(1), match.group(2), match.group(4)


def get_phone_number():
    _, _, phone_number = execute("GET FULL VARIABLE ${CALLERID(num)}")
    return phone_number


def set_variable(name, value):
    execute('SET VARIABLE %s %s' % (name, value))


def add_call_to_db(phone_number):
    cursor = database.cursor()
    query = "INSERT INTO calls(number, started_at) VALUES (?, ?)"
    cursor.execute(query, (phone_number, datetime.now()))
    database.commit()


def count_calls_today(phone_number):
    now = datetime.now()
    today = datetime(now.year, now.month, now.day, 0, 0, 0)
    query = "SELECT COUNT(*) FROM calls WHERE started_at > ? AND number = ?"

    cursor = database.cursor()
    cursor.execute(query, (today,phone_number))

    calls_made = cursor.fetchone()[0]
    logger.info('number of calls for %s: %s', number, calls_made)

    return calls_made


def count_calls_per_minute():
    start = datetime.now() - timedelta(minutes=1)
    query = "SELECT COUNT(*) FROM calls WHERE started_at > ?"

    cursor = database.cursor()
    cursor.execute(query)

    calls_per_minute = cursor.fetchone()[0]
    logger.info('calls per minute: %s', calls_per_minute)

    return calls_per_minute


def count_concurrent_calls():
    execute('SET VARIABLE GROUP() BECKY_CALLS')
    _, _, concurrent_calls = execute('GET FULL VARIABLE ${GROUP_COUNT(BECKY_CALLS)}')
    return concurrent_calls


def get_and_save_number():
    number = get_phone_number()
    add_call_to_db(number)
    return number


def send_spam_alert(number, calls_today, calls_per_minute, concurrent_calls):
    if not config.getboolean('email', 'enabled'):
        return

    mailer = Mailer({'transport.use': 'sendmail'})

    message = Message(author=config.get('mail', 'from'),
                      to=config.get('mail', 'to'))
    message.subject = config.get('mail', 'subject')
    message.plain = EMAIL_MESSAGE.format(number=number,
                                         calls_today=calls_today,
                                         calls_per_minute=calls_per_minute,
                                         concurrent_calls=concurrent_calls)

    mailer.start()
    mailer.send(message)
    mailer.stop()


def main():
    logger.info('script started')

    env = read_env_variables()
    logger.debug('asterisk env: %s', env)

    max_per_minute = config.get('calls', 'max_per_minute')
    max_per_number = config.get('calls', 'max_per_number')
    max_concurrent = config.get('calls', 'max_concurrent')

    concurrent_calls = count_concurrent_calls()
    number = get_and_save_number()
    calls_today = count_calls_today(number)
    calls_per_minute = count_calls_per_minute()

    conditions = [calls_today <= max_per_number,
                  calls_per_minute <= max_per_minute,
                  concurrent_calls <= max_concurrent]

    allowed = all(conditions)

    if not allowed:
        send_spam_alert(number, calls_today, calls_per_minute, concurrent_calls)

    set_variable('CALL_ALLOWED', int(allowed))


if __name__ == "__main__":
    logger.basicConfig(filename=LOG_FILEPATH, level=logging.DEBUG, format=LOG_FORMAT)
    try:
        main()
    except Exception as e:
        logger.exception(str(e), exc_info=True)
        sys.exit(1)
