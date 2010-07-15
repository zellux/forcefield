grammar Expr;

options {
    language=Python;
    output=AST;
    ASTLabelType=CommonTree;
}

tokens {
    NOP; EXPR; BLOCK; TRUE;
}

@header {
import logging

}

/*------------------------------------------------------------------
 * PARSER RULES
 *------------------------------------------------------------------*/

prog
    : ( stmt {if $stmt.tree: logging.debug($stmt.tree.toStringTree());} )+;

stmts
    : (stmt {if $stmt.tree: logging.debug($stmt.tree.toStringTree());} )*
    ;

stmt
    : set_stmt
    | return_stmt
    | if_stmt
    | for_stmt
    | while_stmt
    | NEWLINE ->
    ;

set_stmt
options {
    backtrack=true;
}
    : 'SET' ID '=' expr NEWLINE -> ^('=' ID expr)
    | 'SET' ID '=' expr -> ^('=' ID expr)
    ;

return_stmt
    : 'RETURN' expr NEWLINE -> ^('RETURN' expr)
    ;

if_stmt
options {
    backtrack=true;
}
    : 'IF' expr 'THEN' true_stmts=stmts 'ELSE' false_stmts=stmts 'END' -> ^('IF' ^(EXPR expr) ^(BLOCK $true_stmts) ^(BLOCK $false_stmts))
    | 'IF' expr 'THEN' true_stmts=stmts 'END' -> ^('IF' ^(EXPR expr) ^(BLOCK $true_stmts) ^(BLOCK NOP))
    ;

while_stmt
    : WHILE test_expr=expr 'DO' stmts 'END' -> ^(WHILE ^(EXPR $test_expr) ^(BLOCK stmts))
    ;

for_stmt
options {
    backtrack=true;
}
    : 'FOR' init_stmt=stmt? ';' test_expr=expr ';' post_stmt=stmt? 'DO' stmts 'END' -> ^(BLOCK $init_stmt? ^(WHILE ^(EXPR $test_expr?) ^(BLOCK stmts $post_stmt?)))
    | 'FOR' init_stmt=stmt? ';' WHITESPACE* ';' post_stmt=stmt? 'DO' stmts 'END' -> ^(BLOCK $init_stmt? ^(WHILE ^(EXPR TRUE) ^(BLOCK stmts $post_stmt?)))
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

WHILE : 'WHILE';

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
