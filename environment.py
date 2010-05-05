"""
Maintain environment information
"""
import logging

bindings = {}

def lookup(key):
    if bindings.has_key(key):
        object = bindings[key]
        return object
    else:
        logging.error('Cannot find ' + key + ' in context')
        return None

def set(key, value):
    logging.debug('Set ' + key + ' to ' + unicode(value))
    bindings[key] = value

def add(op1, op2):
    logging.debug('Adding ' + unicode(op1) + ' and ' + unicode(op2))
    if isinstance(op1, int):
        return op1 + op2
    elif isinstance(op1, str) or isinstance(op1, unicode):
        return unicode(op1) + unicode(op2)
    else:
        logging.warning('Unknown type ' + unicode(type(value)))
        
def ret(value):
    logging.debug('Returning ' + unicode(value))
    
