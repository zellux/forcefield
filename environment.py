# -*- coding: utf-8 -*-

"""
Maintain environment information
"""
import logging, sys
import urllib
from datetime import datetime

lastlineno = -1
tracehook = None

def parse_value(value):
    '''Try to detect type of a string. In the order of int > float > string'''
    try:
        x = int(value)
        return x
    except:
        try:
            x = float(value)
            return x
        except:
            return unicode(value, 'utf-8')
            

class ReturnValue(Exception):
    '''Return value to the outer block, by exception mechanism'''
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

class Stmt:
    '''Statement class'''
    def __init__(self, action=None, lineno=-1):
        self.lineno = lineno
        self.action = action
        
    def eval(self):
        '''Called when the statement is actually interpreted'''
        global lastlineno
        lastlineno = self.lineno
        if tracehook != None and self.lineno > 0: tracehook()
        if not self.action:
            logging.warning('scope has no assigned action')
        else:
            self.action()

class Expr:
    '''Expression class'''
    def __init__(self, action=None):
        self.action = action

    def eval(self):
        '''Called when the expression value is actually needed'''
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

    def call(self, values = [], new_binding=True):
        # Return value, i.e., function as expression

        if not self.action:
            logging.warning('Function has no assigned action')
            return

        if len(values) < len(self.paramdef):
            # Given arguments less than parameters, currying
            logging.debug('values=' + repr(values))
            return CurryFunction(values, self.paramdef, self.action)
        
        paramvalues = zip(self.paramdef, values)
        if len(paramvalues) != len(self.paramdef):
            logging.warning('Not enough parameters!')
            
        global current_bindings
        prev = current_bindings
        current_bindings = Binding(current_bindings)
        
        for (k, v) in paramvalues:
            set(k, v, bounded=True)
        
        try:
            logging.debug('call')
            self.action()
            current_bindings = prev
        except ReturnValue, v:
            current_bindings = prev
            logging.debug(repr(v.getValue()))
            return v.getValue()

    def __str__(self):
        return 'Function ' + str(self.paramdef)

    def __repr__(self):
        return 'Function ' + repr(self.paramdef)

    def __unicode__(self):
        return u'Function ' + unicode(self.paramdef)

class CurryFunction(Function):
    '''Currying function'''
    def __init__(self, values=[], paramdef=[], action=None):
        l = len(values)
        self.paramdef = paramdef[l:]
        self.curryvalues = zip(paramdef[:l], values)
        self.nextaction = action
        logging.debug(repr(self.curryvalues))

    def action(self):
        # When this function is called, new environment is already created
        for (k, v) in self.curryvalues:
            set(k, v, bounded=True)
        self.nextaction()
    
class RemoteCall(Function):
    '''Remote call class'''
    def __init__(self, sname, fname, paramdef=[]):
        '''
        sname: script name
        fname: remote function name
        paramdef: parameter definitions'''
        self.sname = sname
        self.fname = fname
        self.paramdef = paramdef
        
    def call(self, values = []):
        '''Similar to what Function.call() does, except that it gets value
        by HTTP requests.'''
        if not server_list.has_key(self.sname):
            logging.error('No such server: %s!' % self.sname)
            return None
        if len(values) != len(self.paramdef):
            logging.warning('Not enough parameters!')

        param = {}
        for k, v in zip(self.paramdef, values):
            param[k] = v
            
        url = server_list[self.sname]
        if len(values) > 0 and not url.endswith('?'):
            url += '?'
        url += urllib.urlencode(param)
        logging.debug(url)
        
        retval = urllib.urlopen(url).read().strip()
        retval = parse_value(retval)
        return retval
        
class Binding(dict):
    '''Binding class'''
    def __init__(self, outer=None):
        dict.__init__(self)
        self.outer = outer

    def dump(self):
        '''Debugging routine for dumping current bindings'''
        sys.stderr.write('Binding dumps\n')
        indent = ['**'] # Hacking for "read-only" Python outer scope binding
        def ptree(d):
            if d.outer != None:
                ptree(d.outer)
            for k, v in d.iteritems():
                value = unicode(v)
                sys.stderr.write((indent[0] + k + ':' + value + '\n').encode('utf-8'))
            indent[0] += '**'
        ptree(self)
        
def fun_WRITE_LOG():
    '''Built-in function WRITE_LOG'''
    f = open("logs.txt", "a")
    f.write(lookup('SYSTEM_LOG').encode('utf-8'))
    f.write('\n')
    f.close()

global_bindings = Binding()
current_bindings = global_bindings

def get_time():
    ret(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

global_bindings[u'SERVER_TIME'] = Function(get_time)
global_bindings[u'WRITE_LOG'] = Function(fun_WRITE_LOG, [u'SYSTEM_LOG'])

def lookup(key, binding=None, allow_null=False):
    '''Lookup variable value in current scope, if not found, go to outer scope'''
    if binding == None:
        binding = current_bindings
        
    if binding.has_key(key):
        object = binding[key]
        return object
    else:
        if binding.outer != None:
            return lookup(key, binding.outer)
        if not allow_null:
            logging.error('Cannot find ' + key + ' in context')
        return None
    
def set(key, value, binding=None, bounded=False):
    '''Set _value_ to variable named _key_, within given _binding_.
    When bounded is False, the method will search for outer scope when
    _key_ is not found in current scope, otherwise it will simply
    set current scope'''

    if not binding:
        binding = current_bindings
    b = binding
    logging.debug('Set ' + key + ' to ' + repr(value))
    if bounded:
        binding.__setitem__(key, value)
        return
    # Lookup key from inner scope to outer scope
    while True:
        if b.has_key(key):
            b[key] = value
            return True
        b = b.outer
        if b == None: break
        
    binding.__setitem__(key, value)

def add(op1, op2):
    '''Add op1 and op2'''
    logging.debug('Adding ' + repr(op1) + ' and ' + repr(op2))
    if isinstance(op1, int) or isinstance(op1, float):
        return op1 + op2
    elif isinstance(op1, str) or isinstance(op1, unicode):
        return op1 + unicode(op2)
    else:
        logging.warning('Unknown type ' + str(type(op1)))

def ret(value):
    '''Return value by raising an exception'''
    logging.debug('Returning ' + unicode(value))
    raise ReturnValue(value)

# Initialize server list
server_list = {}

f = open('server.conf', 'r')
for line in f.readlines():
    pair = map(str.strip, line.split(','))
    if len(pair) < 2: continue
    server_list[unicode(pair[0])] = unicode(pair[1])

