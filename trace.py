#/usr/bin/python

import sys, logging, getopt, signal, os, time
import base64
import environment
import antlr3
import antlr3.tree
from environment import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr3 import RecognitionException
import Eval
import traceback

wakeup = True

def handler(signum, stack):
    global wakeup
    wakeup = True
    
def interative_hook():
    current_bindings.dump()
    global wakeup
    wakeup = False
    while not wakeup:
        time.sleep(5)
    
if __name__ == '__main__':
    Eval.tracehook = interative_hook
    signal.signal(signal.SIGUSR1, handler)
    
    char_stream = antlr3.ANTLRInputStream(sys.stdin, encoding='utf-8')
    lexer = ExprLexer(char_stream)
    tokens = antlr3.CommonTokenStream(lexer)
    parser = ExprParser(tokens)
    r = parser.prog()
    root = r.tree
    nodes = antlr3.tree.CommonTreeNodeStream(root)
    walker = Eval.Eval(nodes)

    try:
        for e in walker.prog():
            print e
    except ReturnValue, v:
        if isinstance(v.getValue(), str) or isinstance(v.getValue(), unicode):
            print v.getValue().encode('utf-8')
        else:
            print v.getValue()
    except RecognitionException:
        traceback.print_stack()

