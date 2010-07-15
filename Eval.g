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

prog
    : (x=stmt {if x: x.eval()}) + ;

code_block returns [scope]
@init {
    l = []
}
    : ^(BLOCK (s=stmt {l.append(s)}) *) {
            def action():
                for x in l:
                    x.eval()
            return Scope(action)
        }
    ;

stmt returns [scope]
    : ^('=' ID expr) {
            $scope = Scope(lambda: set($ID.text, $expr.value.eval()))}
    | code_block { $scope = $code_block.scope }
    | NOP { $scope = Expr(lambda: None) }
    | ^('RETURN' expr) {
            $scope = Scope(lambda: ret($expr.value.eval()))}
    | ^('IF' ^(EXPR v=expr) t=code_block f=code_block) {
            def action():
                if v.eval():
                    t.eval()
                else:
                    f.eval()
            $scope = Scope(action)}
    | ^(WHILE ^(EXPR test=expr?) body=code_block) {
            def action():
                while test.eval():
                    body.eval()
            $scope = Scope(action)}
    ;

expr returns [value]
    : ^('==' a=expr b=expr) {$value = Expr(lambda: a.eval() == b.eval())}
    | ^('<' a=expr b=expr) { $value = Expr(lambda: a.eval() < b.eval()) }
    | ^('+' a=expr b=expr) {$value = Expr(lambda: add(a.eval(), b.eval()))}
    | ^('-' a=expr b=expr) {$value = Expr(lambda: a.eval() - b.eval())}
    | ^('*' a=expr b=expr) {$value = Expr(lambda: a.eval() * b.eval())}
    | ID {$value = Expr(lambda: lookup($ID.text))}
    | ^(ID e=expr) {$value = Expr(lambda: lookup($ID.text)[e.eval()])}
    | STRING_LITERAL {$value = Expr(lambda: $STRING_LITERAL.text)}
    | NUMBER {$value = Expr(lambda: int($NUMBER.text))}
    | TRUE { $value = Expr(lambda: True)}
    ;

