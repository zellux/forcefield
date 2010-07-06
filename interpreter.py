#!/usr/bin/bash

"""
Interprete the given file

Usage: python interpreter.py [--nodebug] [--param=<param>]
"""

import sys
import logging
import getopt
import base64
import environment
from antlr3 import *
from environment import *
from CloudScriptLexer import CloudScriptLexer
from CloudScriptParser import CloudScriptParser

def parse():
    char_stream = ANTLRInputStream(sys.stdin, encoding='utf-8')
    lexer = CloudScriptLexer(char_stream)
    tokens = CommonTokenStream(lexer)
    parser = CloudScriptParser(tokens)

    try:
        parser.stmts()
    except ReturnValue as v:
        print v.getValue()
    except RecognitionException:
        traceback.print_stack()

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "", ["help", "nodebug", "param="])
    
    debug = True
    for opt, arg in opts:
        if opt in ('--nodebug'):
            debug = False
        if opt in ('--param'):
            params = eval(base64.b64decode(arg))
            for key in params.iterkeys():
                params[key] = unicode(params[key][0], 'utf-8')
	    environment.bindings['HTTP'] = params
            
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    parse()
