#!/usr/bin/bash

from antlr3 import *
from CloudScriptLexer import CloudScriptLexer
from CloudScriptParser import CloudScriptParser

if __name__ == '__main__':
    char_stream = ANTLRFileStream(sys.argv[1], encoding='utf-8')
    lexer = CloudScriptLexer(char_stream)
    tokens = CommonTokenStream(lexer)
    parser = CloudScriptParser(tokens);

    try:
        parser.stmts()
    except RecognitionException:
        traceback.print_stack()
