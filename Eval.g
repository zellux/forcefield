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
            return Stmt(action)
        }
    ;

stmt returns [scope]
@init {
}
    : ^('=' ID expr) {
            $scope = Stmt(lambda: set($ID.text, $expr.value.eval()), $ID.token.line) }
    | ^('=' ^(DICT ID index=expr) e=expr) {
            def action():
                d = lookup($ID.text, allow_null=True)
                if d == None:
                    d = {}
                    set($ID.text, d)
                idx = index.eval()
                val = e.eval()
                logging.debug('Set %s[%s] to %s' % ($ID.text, repr(idx), repr(val)))
                d[idx] = val
            $scope = Stmt(action, $ID.token.line) }
    | code_block { $scope = $code_block.scope }
    | NOP { $scope = Expr(lambda: None) }
    | ^(RETURN expr) {
            $scope = Stmt(lambda: ret($expr.value.eval()), $RETURN.token.line) }
    | ^(IF ^(EXPR v=expr) t=code_block f=code_block) {
            def action():
                if v.eval():
                    t.eval()
                else:
                    f.eval()
            $scope = Stmt(action, $IF.token.line) }
    | ^(WHILE ^(EXPR test=expr?) body=code_block) {
            def action():
                while test.eval():
                    body.eval()
            $scope = Stmt(action, $WHILE.token.line) }
    | ^(ASSERT v=expr) {
            def action():
                if not v.eval():
                    logging.error("Assert failed!")
                    sys.exit(-1)

            $scope = Stmt(action, $ASSERT.token.line) }
    | call { $scope = Stmt(lambda: $call.value.eval(), $call.line) }
    | remote_stmt { $scope = $remote_stmt.scope }
    | func_stmt { $scope = $func_stmt.scope }
    ;

remote_stmt returns [scope]
@init {
    l = []
}
    : ^(REMOTE sname=SID fname=ID ^(PARAMLIST (id=ID { l.append(id.text) })*)) {
            f = RemoteCall(sname.text, fname.text, l)
            return Stmt(lambda: set(fname.text, f), $REMOTE.token.line)
        }
    ;

func_stmt returns [scope]
@init {
    l = []
}
    : ^(FUNC fname=ID ^(PARAMLIST (id=ID { l.append(id.text) })*) body=code_block) {
            def action():
                body.eval()
            f = Function(action, l)
            return Stmt(lambda: set(fname.text, f), $FUNC.token.line)
        }
    ;

call returns [value, line]
@init {
    l = []
}
    : ^(CALL ID ^(ARGLIST (e=expr { l.append(e) })*)) {
        def callfunc():
            defun = lookup($ID.text)
            if not isinstance(defun, Function) and not isinstance(defun, RemoteCall):
                logging.error("Function " + $ID.text + " was not defined")
                return None
            else:
                return defun.call(map(lambda x: x.eval(), l))
        $value = Expr(callfunc)
        $line=$ID.token.line}
    ;

expr returns [value]
    : ^('==' a=expr b=expr) { $value = Expr(lambda: a.eval() == b.eval()) }
    | ^('<=' a=expr b=expr) { $value = Expr(lambda: a.eval() <= b.eval()) }
    | ^('>=' a=expr b=expr) { $value = Expr(lambda: a.eval() >= b.eval()) }
    | ^('<>' a=expr b=expr) { $value = Expr(lambda: a.eval() <> b.eval()) }
    | ^('<' a=expr b=expr) { $value = Expr(lambda: a.eval() < b.eval()) }
    | ^('>' a=expr b=expr) { $value = Expr(lambda: a.eval() > b.eval()) }
    | ^('+' a=expr b=expr) { $value = Expr(lambda: add(a.eval(), b.eval())) }
    | ^('-' a=expr b=expr) { $value = Expr(lambda: a.eval() - b.eval()) }
    | ^('*' a=expr b=expr) { $value = Expr(lambda: a.eval() * b.eval()) }
    | ^(AND a=expr b=expr) { $value = Expr(lambda: a.eval() and b.eval()) }
    | ^(OR a=expr b=expr) { $value = Expr(lambda: a.eval() or b.eval()) }
    | ^(NOT a=expr) { $value = Expr(lambda: not a.eval()) }
    | ID {$value = Expr(lambda: lookup($ID.text))}
    | ^(DICT ID e=expr) {$value = Expr(lambda: lookup($ID.text)[e.eval()])}
    | call { $value = $call.value }
    | STRING_LITERAL { $value = Expr(lambda: $STRING_LITERAL.text) }
    | INTEGER { $value = Expr(lambda: int($INTEGER.text)) }
    | FLOAT { $value = Expr(lambda: float($FLOAT.text)) }
    | TRUE { $value = Expr(lambda: True) }
    ;

