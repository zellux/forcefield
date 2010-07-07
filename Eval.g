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

stmt : ^('=' ID expr)
        {set($ID.text, $expr.value);}
    | ^('RETURN' expr)
        {ret($expr.value);}
    | 'IF' expr (stmt) 'ELSE' (stmt)
        {}
    ;

expr returns [value]
    : ^('--' a=expr b=expr) {$value = a == b;}
    | ^('+' a=expr b=expr) {$value = add(a, b);}
    | ^('-' a=expr b=expr) {$value = a - b;}
    | ^('*' a=expr b=expr) {$value = a * b;}
    | ID {$value = lookup($ID.text);}
    | ^(ID e=expr) {dict = lookup($ID.text); $value = dict[e];}
    | STRING_LITERAL {$value = $STRING_LITERAL.text;}
    ;

