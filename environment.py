"""
Maintain environment information
"""
import logging

bindings = {}

def lookup(key):
    if bindings.has_key(key):
        return bindings[key]
    else:
        logging.error('Cannot find ' + key + ' in context')
        return None

def set(key, value):
    logging.debug('SET ' + key + ' TO ' + str(value))
    bindings[key] = value

