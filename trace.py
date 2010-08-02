#!/usr/bin/python

''' Debugging program given by stdin.
stderr for debugging information
stdout for program output
'''

import sys, logging, getopt, signal, os, time
import base64
import environment
import antlr3
import antlr3.tree
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr3 import RecognitionException
import Eval
import traceback
from interpreter import interpret, parse

wakeup = True

def handler(signum, stack):
    global wakeup
    wakeup = True
    
def interative_hook():
    environment.current_bindings.dump()
    sys.stdout.write('END\n')
    sys.stdout.flush()
    sys.stderr.write('# ' + str(environment.lastlineno) + '\n')
    sys.stderr.write('END\n')
    sys.stderr.flush()
    global wakeup
    wakeup = False
    while not wakeup:
        time.sleep(5)

if __name__ == '__main__':
    environment.tracehook = interative_hook
    signal.signal(signal.SIGUSR1, handler)
    
    interpret()
    parse()
    
    sys.stdout.write('TERMINATED\n')
    sys.stdout.flush()
    sys.stderr.write('TERMINATED\n')
    sys.stderr.flush()
