# -*- coding: utf-8 -*-

"""
Maintain environment information
"""
import logging

bindings = {}

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value.encode('utf-8')

    def getValue(self):
        return self.value

def lookup(key):
    if bindings.has_key(key):
        object = bindings[key]
        return object
    else:
        logging.error('Cannot find ' + key + ' in context')
        return None

def set(key, value):
    logging.debug('Set ' + key + ' to ' + repr(value))
    bindings[key] = value

def add(op1, op2):
    logging.debug('Adding ' + repr(op1) + ' and ' + repr(op2))
    if isinstance(op1, int):
        return op1 + op2
    elif isinstance(op1, str) or isinstance(op1, unicode):
        return op1 + unicode(op2)
    else:
        logging.warning('Unknown type ' + str(type(op1)))

def ret(value):
    logging.debug('Returning ' + unicode(value))
    raise ReturnValue(value)

