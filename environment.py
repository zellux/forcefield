# -*- coding: utf-8 -*-

"""
Maintain environment information
"""
import logging
from datetime import datetime

bindings = {}

class ReturnValue(Exception):
    def __init__(self, value):
        if type(value) == type(''):
            self.value = value.encode('utf-8')
        else:
            self.value = unicode(value).encode('utf-8')

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

class Scope:
    def __init__(self, action=None):
        self.action = action

    def eval(self):
        if not self.action:
            logging.warning('scope has no assigned action')
        else:
            self.action()

class Expr:
    def __init__(self, action=None):
        self.action = action

    def eval(self):
        if not self.action:
            logging.warning('expression has no assigned action')
        else:
            return self.action()

class Defun:
    '''方法定义'''
    def __init__(self, action=None, paramdef=[]):
        self.action = action
        self.paramdef = paramdef

    def call(self, values = []):
        paramvalues = zip(self.paramdef, values)
        if len(paramvalues) != len(self.paramdef):
            logging.warning('Not enough parameters!')
        for (k, v) in paramvalues:
            set(k, v)
        if not self.action:
            logging.warning('Function has no assigned action')
        else:
            return self.action()

    def eval(self):
        return None

def fun_WRITE_LOG():
    f = open("logs.txt", "a")
    with f:
        f.write(lookup('SYSTEM_LOG'))
        f.write('\n')

bindings['SERVER_TIME'] = Defun(lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
bindings['WRITE_LOG'] = Defun(fun_WRITE_LOG, ['SYSTEM_LOG'])
