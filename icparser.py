#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyparsing import *

decimalNumber = Word(nums) + Optional("." + OneOrMore(Word(nums)))
operand = decimalNumber | quotedString.setParseAction(lambda ts: ts[0][1:-1])
signop = oneOf("+ -")
multop = oneOf("* /")
plusop = oneOf("+ -")
arithmaticExpr = operatorPrecedence(operand,
        [(signop, 1, opAssoc.RIGHT),
            (multop, 2, opAssoc.LEFT),
            (plusop, 2, opAssoc.LEFT),])

def __numberParse(tokens):
    if tokens[0].find(".") >= 0:
        return float(tokens[0])
    else:
        return int(tokens[0])

decimalNumber.setParseAction(lambda ts: "".join(ts), __numberParse)

if __name__ == "__main__":
    print decimalNumber.parseString("3.1415926")
    print arithmaticExpr.parseString("1 + 2.34 * 3 / 4.57 + 'test' + 3")
