tree grammar Eval;

options {
    language=Python;
    tokenVocab=Expr;
    ASTLabelType=CommonTree;
}

@header {
import sys
import traceback
import logging

from environment import *
from ExprLexer import ExprLexer

}

prog : stmt+ ;

stmts
    : stmt* 
    ;

if_branch
@init {
    #print "[Test side effect]"
}
    : ^(BLOCK stmts)
    ;

if_stmt
@after {
    logging.debug("TEST expr=" + str($v.value))
    stmtsNode = None
    if $v.value:
        stmtsNode = $if_stmt.start.getChild(1)
    else:
        stmtsNode = $if_stmt.start.getChild(2)
    self.input.push(self.input.getNodeIndex(stmtsNode))
    self.if_branch()
    self.input.pop()
}
    : ^('IF' ^(EXPR v=expr) . .)
    ;

stmt
    : ^('=' ID expr)
        {set($ID.text, $expr.value);}
    | ^('RETURN' expr)
        {ret($expr.value);}
    | if_stmt
    ;

expr returns [value]
    : ^('==' a=expr b=expr) {$value = a == b;}
    | ^('+' a=expr b=expr) {$value = add(a, b);}
    | ^('-' a=expr b=expr) {$value = a - b;}
    | ^('*' a=expr b=expr) {$value = a * b;}
    | ID {$value = lookup($ID.text);}
    | ^(ID e=expr) {dict = lookup($ID.text); $value = dict[e];}
    | STRING_LITERAL {$value = $STRING_LITERAL.text;}
    ;

