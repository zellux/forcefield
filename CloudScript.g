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

from environment import *
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
        ('+' e=multExpr {$value = add($value, $e.value);}
        |'-' e=multExpr {$value -= $e.value;}
        )*
    ;

multExpr returns [value]
    : e=atom {$value = $e.value;}
        ('*' e=atom {$value *= $e.value;})*
    ;
    
atom returns [value]
    : NUMBER {$value = int($NUMBER.text);}
    | ID {$value = lookup($ID.text);}
    | STRING_LITERAL {$value = $STRING_LITERAL.text;}
    | '(' expr ')'
    ;

set_stmt : 'SET' ID '=' expr {set($ID.text, $expr.value);};

return_stmt : 'RETURN' expr {ret($expr.value);};
        
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
STRING_LITERAL : '"' (.)* '"' {self.text = self.text[1:-1];};
NEWLINE : '\r'? '\n';

fragment DIGIT : '0'..'9' ;

ID: LETTER (LETTER | DIGIT | '_')*;
