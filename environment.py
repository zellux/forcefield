# -*- coding: utf-8 -*-

"""
Maintain environment information
"""
import logging
from datetime import datetime

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

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

class Function:
    '''Function object '''
    def __init__(self, action=None, paramdef=[]):
        '''
        Parameters:
        action: function behaviour
        paramdef: a list of function parameters, which will be used
                  for dictionary keys when the function is called
        '''
        self.action = action
        self.paramdef = paramdef

    def call(self, values = []):
        # Return value, i.e., function as expression

        if not self.action:
            logging.warning('Function has no assigned action')
            return
        
        paramvalues = zip(self.paramdef, values)
        if len(paramvalues) != len(self.paramdef):
            logging.warning('Not enough parameters!')
        for (k, v) in paramvalues:
            set(k, v)
        
        global current_bindings
        prev = current_bindings
        current_bindings = Binding(current_bindings)
        try:
            self.action()
            current_bindings = prev
        except ReturnValue as v:
            current_bindings = prev
            return v.getValue()

class Binding(dict):
    def __init__(self, outer=None):
        dict.__init__(self)
        self.outer = outer
        
def fun_WRITE_LOG():
    f = open("logs.txt", "a")
    with f:
        f.write(lookup('SYSTEM_LOG'))
        f.write('\n')

global_bindings = Binding()
current_bindings = global_bindings

global_bindings['SERVER_TIME'] = Function(lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
global_bindings['WRITE_LOG'] = Function(fun_WRITE_LOG, ['SYSTEM_LOG'])

def lookup(key, binding=current_bindings):
    if binding.has_key(key):
        object = binding[key]
        return object
    else:
        if binding.outer != None:
            return lookup(key, binding)
        logging.error('Cannot find ' + key + ' in context')
        return None
    
def set(key, value, binding=current_bindings):
    b = binding
    logging.debug('Set ' + key + ' to ' + repr(value))
    # Lookup key from inner scope to outer scope
    while True:
        if b.has_key(key):
            b[key] = value
            return True
        b = b.outer
        if b == None: break
        
    binding.__setitem__(key, value)
    return False

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

