grammar Expr;

options {
    language=Python;
    output=AST;
    ASTLabelType=CommonTree;
}

@header {
import logging

}

/*------------------------------------------------------------------
 * PARSER RULES
 *------------------------------------------------------------------*/

prog
    : ( stmt {if $stmt.tree: logging.debug($stmt.tree.toStringTree());} )+;

stmt
    : set_stmt
    | return_stmt
    | if_stmt
    | NEWLINE ->
    ;

set_stmt
    : 'SET' ID '=' expr NEWLINE -> ^('=' ID expr)
    ;

return_stmt
    : 'RETURN' expr NEWLINE -> ^('RETURN' expr)
    ;

if_stmt
    : 'IF'^ expr 'THEN'! (stmt)* ('ELSE' (stmt)*)? 'END'!
    ;

atom
    : NUMBER
    | ID
    | ID '[' expr ']' -> ^(ID expr)
    | STRING_LITERAL
    | '('! expr ')'!
    ;

boolNeg
    : ('not'^)? atom
    ;

signExpr
    : (('+'^|'-'^))? boolNeg
    ;

multExpr
    : signExpr (('*'^|'/'^|'mod'^) signExpr)*
    ;

addExpr
    : multExpr (('+'^|'-'^) multExpr)*
    ;

relExpr
    : addExpr (('=='^|'!='^|'>='^|'<='^|'>'^|'<'^) addExpr)* 
    ;

expr
    : relExpr (('and'^|'or'^) relExpr)*
    ;

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
