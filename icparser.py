#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyparsing import *

decimalNumber = Word(nums) + Optional("." + OneOrMore(Word(nums)))
operand = decimalNumber | quotedString #.setParseAction(lambda ts: ts[0][1:-1])
signop = oneOf("+ -")
multop = oneOf("* /")
plusop = oneOf("+ -")
arithmaticExpr = operatorPrecedence(operand,
        [(signop, 1, opAssoc.RIGHT),
            (multop, 2, opAssoc.LEFT),
            (plusop, 2, opAssoc.LEFT),])

# 整型值
ic_bininteger = "0" + oneOf("b B") + Word("01")
ic_octinteger = "0" + Suppress(Optional(oneOf("o O"))) + Word("01234567")
ic_hexinteger = "0" + oneOf("x X") + Word(hexnums)
ic_decimalinteger = (Regex("[1-9]") + Word(nums)) | Literal("0")
ic_integer = ic_bininteger | ic_octinteger | ic_hexinteger | ic_decimalinteger
#ic_longinteger = ic_integer + oneOf("l L")

ic_bininteger.setParseAction(lambda ts: "".join(ts), lambda ts: int(ts[0], 2))
ic_octinteger.setParseAction(lambda ts: "".join(ts), lambda ts: int(ts[0], 8))
ic_hexinteger.setParseAction(lambda ts: "".join(ts), lambda ts: int(ts[0], 16))
ic_decimalinteger.setParseAction(lambda ts: "".join(ts), lambda ts: int(ts[0]))

# 浮点值
ic_exponent = oneOf("e E") + Optional(oneOf("+ -")) + Word(nums)
ic_fraction = "." + Word(nums)
ic_intpart = Word(nums)
ic_pointfloat = (Optional(ic_intpart) + ic_fraction) | (ic_intpart + ".")
ic_exponentfloat = (ic_pointfloat | ic_intpart) + ic_exponent
ic_floatnumber = ic_exponentfloat | ic_pointfloat

ic_floatnumber.setParseAction(lambda ts: "".join(ts), lambda ts: float(ts[0]))

# 数值
ic_number = ic_floatnumber | ic_integer

# 命名标识
ic_identifier = Combine(Regex("[a-zA-Z_]") + Optional(Word(alphanums + "_")))

# 关键字
ic_keyword = oneOf("SET RETURN IF THEN ELSE END FUNC")

# 表达式
ic_signop = oneOf("+ -")
ic_multop = oneOf("* / %")
ic_plusop = oneOf("+ -")
ic_expr = Forward()
ic_increment = Group((oneOf("++ --") + ic_identifier) | (ic_identifier + oneOf("++ --")))
ic_arithmetic_operand = Group(Optional(ic_signop) +\
    (ic_increment | ic_number | ic_identifier | quotedString |
            Group(Suppress("(") + ZeroOrMore(ic_expr) + Suppress(")"))))
ic_expr << ic_arithmetic_operand + ZeroOrMore((ic_multop | ic_plusop) + ic_arithmetic_operand)

def __removeListWrapper(tokens):
    if len(tokens[0]) == 1:
        return tokens[0]
    else:
        return tokens

ic_arithmetic_operand.setParseAction(__removeListWrapper)

def __groupExpr(tokens):
    '''因为未做加法和乘法的优先级的判断，所以准备用个方法把这事做了'''
    if len(tokens) < 5:
        return tokens
    stack = []
    stack.append(tokens[0])
    for (i, v) in enumerate(tokens[1:]):
        if (i % 2 == 0):
            if "*/%".find(v) >= 0:
                top = stack.pop()
                if type(top) == type([]):
                    top.append(v)
                else:
                    top = [top, v]
                stack.append(top)
            else:
                stack.append(v)
        else:
            top = stack.pop()
            if type(top) == type([]):
                top.append(v)
                stack.append(top)
            else:
                stack.append(top)
                stack.append(v)
    return stack

if __name__ == "__main__":
    print ic_expr.parseString("+123+ +1231.123e11*_abc/(.23e10 - incr++) + 'test string' + () + \"def\"")
    ic_expr.setParseAction(__groupExpr)
    #print ic_identifier.parseString("_32342")
    print ic_expr.parseString("+123+ +1231.123e11*_abc/(.23e10 - incr++) + 'test string' + () + \"def\"")
