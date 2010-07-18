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
import pdb

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
    | ^('ASSERT' v=expr) {
            def action():
                if not v.eval():
                    logging.error("Assert failed!")
                    sys.exit(-1)

            $scope = Scope(action)}
    | call { $scope = Scope(lambda: $call.value.eval()) }
    | func_stmt {$scope = $func_stmt.scope}
    ;

func_stmt returns [scope]
@init {
    l = []
}
    : ^('FUNC' fname=ID ^(PARAMLIST (ID { l.append(id) })*) body=code_block) {
            def action():
                body.eval()
            f = Function(action)
            return Scope(lambda: set(fname.text, f))
        }
    ;

call returns [value]
@init {
    l = []
}
    : ^(CALL ID ^(ARGLIST (e=expr { l.append(e) })*)) {
        def callfunc():
            defun = lookup($ID.text)
            if not isinstance(defun, Function):
                logging.debug("Function " + $ID.text + " was not defined")
                return None
            else:
                return defun.call(map(lambda x: x.eval(), l))
        $value = Expr(callfunc)}
    ;

expr returns [value]
    : ^('==' a=expr b=expr) { $value = Expr(lambda: a.eval() == b.eval()) }
    | ^('<' a=expr b=expr) { $value = Expr(lambda: a.eval() < b.eval()) }
    | ^('+' a=expr b=expr) { $value = Expr(lambda: add(a.eval(), b.eval())) }
    | ^('-' a=expr b=expr) { $value = Expr(lambda: a.eval() - b.eval()) }
    | ^('*' a=expr b=expr) { $value = Expr(lambda: a.eval() * b.eval()) }
    | ID {$value = Expr(lambda: lookup($ID.text))}
    | ^(ID e=expr) {$value = Expr(lambda: lookup($ID.text)[e.eval()])}
    | call { $value = $call.value }
    | STRING_LITERAL {$value = Expr(lambda: $STRING_LITERAL.text)}
    | NUMBER {$value = Expr(lambda: int($NUMBER.text))}
    | TRUE { $value = Expr(lambda: True)}
    ;

