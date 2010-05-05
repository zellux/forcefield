#!/usr/bin/bash

import sys
from antlr3 import *
from CloudScriptLexer import CloudScriptLexer
from CloudScriptParser import CloudScriptParser

def parse(filename):
    char_stream = ANTLRFileStream(filename, encoding='utf-8')
    lexer = CloudScriptLexer(char_stream)
    tokens = CommonTokenStream(lexer)
    parser = CloudScriptParser(tokens)

    try:
        parser.stmts()
    except RecognitionException:
        traceback.print_stack()

if __name__ == '__main__':
    parse(sys.argv[1])
