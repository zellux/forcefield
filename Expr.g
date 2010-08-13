grammar Expr;

options {
    language=Python;
    output=AST;
    ASTLabelType=CommonTree;
}

tokens {
    NOP; EXPR; BLOCK; TRUE; CALL; PARAMLIST; ARGLIST; DICT;
    ASSERT = 'ASSERT';
    RETURN = 'RETURN';
    IF = 'IF';
    ELSE = 'ELSE';
    END = 'END';
    SET = 'SET';
    FUNC = 'FUNC';
    THEN = 'THEN';
    DO = 'DO';
    FOR = 'FOR';
    REMOTE = 'REMOTE';
    WHILE = 'WHILE';
    AND = 'AND';
    OR = 'OR';
    NOT = 'NOT';
    TO = 'TO';
    STEP = 'STEP';
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
    : (stmt)*
    ;

stmt
    : set_stmt
    | return_stmt
    | if_stmt
    | for_stmt
    | while_stmt
    | call_stmt
    | func_stmt
    | assert_stmt
    | remote_stmt
    | NEWLINE -> NOP
    ;

set_stmt
options {
    backtrack=true;
}
    : SET ID '=' expr -> ^('=' ID expr)
    | SET dict '=' expr -> ^('=' dict expr)
    ;

return_stmt
    : RETURN expr -> ^(RETURN expr)
    ;

if_stmt
options {
    backtrack=true;
}
    : IF expr THEN t=stmts ELSE f=stmts END ->
        ^(IF ^(EXPR expr) ^(BLOCK $t) ^(BLOCK $f))
    | IF expr THEN t=stmts END ->
        ^(IF ^(EXPR expr) ^(BLOCK $t) ^(BLOCK NOP))
    ;

while_stmt
    : WHILE test=expr DO stmts END -> ^(WHILE ^(EXPR $test) ^(BLOCK stmts))
    ;

for_stmt
options {
    backtrack=true;
}
    : FOR i=expr '=' init=expr TO fin=expr STEP step=expr DO stmts END
        -> ^(BLOCK ^('=' $i $init)
            ^(WHILE ^(EXPR ^('<=' $i $fin))
                ^(BLOCK stmts ^('=' $i ^('+' $i $step)))))
    ;

assert_stmt
    : ASSERT expr -> ^(ASSERT expr)
    ;

func_stmt
    : FUNC ID '(' param_list ')' stmts END -> ^(FUNC ID param_list ^(BLOCK stmts))
    ;

remote_stmt
    : REMOTE SID ID '(' param_list ')' -> ^(REMOTE SID ID param_list)
    ;

param_list
    : (ID (',' ID)*)? -> ^(PARAMLIST ID*)
    ;


arg_list
    : (expr (',' expr)*)? -> ^(ARGLIST expr*)
    ;

call_stmt
    : callExpr
    ;

dict
    : ID '[' expr ']' -> ^(DICT ID expr)
    ;

atom
    : INTEGER
    | FLOAT
    | ID
    | callExpr
    | dict
    | STRING_LITERAL
    | '('! expr ')'!
    ;

callExpr
    : ID '(' arg_list ')' -> ^(CALL ID arg_list)
    ;

boolNeg
    : (NOT^)? atom
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
    : relExpr ((AND^|OR^) relExpr)*
    ;

/*------------------------------------------------------------------
 * LEXER RULES
 *------------------------------------------------------------------*/

INTEGER: ('0'..'9')+;
FLOAT: INTEGER '.' INTEGER;

fragment LETTER: LOWER | UPPER;
fragment LOWER: 'a'..'z';
fragment UPPER: 'A'..'Z';
fragment SPACE: ' ' | '\t';

WHITESPACE: SPACE+ { $channel = HIDDEN;};
STRING_LITERAL : '"' (.)* '"' {self.text = self.text[1:-1];};
NEWLINE : '\r'? '\n';

fragment DIGIT : '0'..'9' ;

ID: LETTER (LETTER | DIGIT | '_')*;
SID: '@' ID {self.text = self.text[1:]};
