#!/usr/bin/python

"""
Interprete the given file

Usage: python interpreter.py [--nodebug] [--param=<param>]
"""

import sys
import logging
import getopt
import base64
import environment
import antlr3
import antlr3.tree
from environment import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr3 import RecognitionException
import Eval

def parse():
    char_stream = antlr3.ANTLRInputStream(sys.stdin, encoding='utf-8')
    lexer = ExprLexer(char_stream)
    tokens = antlr3.CommonTokenStream(lexer)
    parser = ExprParser(tokens)
    r = parser.prog()
    root = r.tree
    nodes = antlr3.tree.CommonTreeNodeStream(root)
    walker = Eval.Eval(nodes)

    try:
        walker.prog()
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
