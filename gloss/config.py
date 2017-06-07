"""Handles application-wide configurations.
"""

from ConfigParser import ConfigParser


config = ConfigParser()
config.read('gloss/config.ini')

db_connection_args = {
    'user': config.get('db', 'user'),
    'passwd': config.get('db', 'passwd'),
    'db': config.get('db', 'db'),
    'host': config.get('db', 'host')
}
