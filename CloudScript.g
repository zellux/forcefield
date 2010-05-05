grammar CloudScript;

options {
    language = Python;
}

tokens {
    PLUS = '+' ;
    MINUS = '-' ;
    MULT = '*' ;
    DIV = '/' ;
    EQUALS = '=';
    SET = 'SET';
    RETURN = 'RETURN';
}

@header {
import sys
import traceback

from CloudScriptLexer import CloudScriptLexer
}

@main {
def main(argv, otherArg=None):
  char_stream = ANTLRFileStream(sys.argv[1])
  lexer = CloudScriptLexer(char_stream)
  tokens = CommonTokenStream(lexer)
  parser = CloudScriptParser(tokens);

  try:
        parser.stmts()
  except RecognitionException:
    traceback.print_stack()
}

/*------------------------------------------------------------------
 * PARSER RULES
 *------------------------------------------------------------------*/

stmts : stmt (NEWLINE stmt)* NEWLINE*;

expr : term ( ( PLUS | MINUS )  term )* ;

term : factor ( ( MULT | DIV ) factor )* ;

factor : NUMBER | STRING_LITERAL | NAME;

set_stmt : SET NAME EQUALS expr;

return_stmt : RETURN expr;
        
stmt : set_stmt | return_stmt;

/*------------------------------------------------------------------
 * LEXER RULES
 *------------------------------------------------------------------*/

NUMBER : INTEGER;
fragment INTEGER: '0' | (PLUS|MINUS)? '1'..'9' '0'..'9'*;

fragment LETTER: LOWER | UPPER;
fragment LOWER: 'a'..'z';
fragment UPPER: 'A'..'Z';
fragment SPACE: ' ' | '\t';

WHITESPACE: SPACE+ { $channel = HIDDEN;};
STRING_LITERAL : '"' (.)* '"';
NEWLINE : '\r'? '\n';

fragment DIGIT : '0'..'9' ;

NAME: LETTER (LETTER | DIGIT | '_')*;
