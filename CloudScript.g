grammar CloudScript;

options {
    language = Python;
}

// tokens {
// }

@header {
import sys
import traceback
import logging

from CloudScriptLexer import CloudScriptLexer

logging.basicConfig(level=logging.DEBUG)
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

// TODO: support multiple operators, for example, a+b+c
// TODO: support parenthesis

stmts : stmt (NEWLINE+ stmt)* NEWLINE*;

expr returns [value]
    : e=multExpr {value = $e.value;}
        ('+' e=multExpr {$value += $e.value;}
        |'-' e=multExpr {$value -= $e.value;}
        )*
    ;

multExpr returns [value]
    : e=atom {$value = $e.value;}
        ('*' e=atom {$value *= $e.value;})*
    ;
    
atom returns [value]
    : NUMBER {$value = int($NUMBER.text);}
    | ID
    | '(' expr ')'
    ;

set_stmt : 'SET' ID '=' expr {logging.debug('SET ' + $ID.text + ' TO ' + str($expr.value));};

return_stmt : 'RETURN' expr;
        
stmt : set_stmt | return_stmt;

/*------------------------------------------------------------------
 * LEXER RULES
 *------------------------------------------------------------------*/

NUMBER : INTEGER;
fragment INTEGER: '0' | '1'..'9' '0'..'9'*;

fragment LETTER: LOWER | UPPER;
fragment LOWER: 'a'..'z';
fragment UPPER: 'A'..'Z';
fragment SPACE: ' ' | '\t';

WHITESPACE: SPACE+ { $channel = HIDDEN;};
STRING_LITERAL : '"' (.)* '"';
NEWLINE : '\r'? '\n';

fragment DIGIT : '0'..'9' ;

ID: LETTER (LETTER | DIGIT | '_')*;
