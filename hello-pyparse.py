#!/usr/bin/python

from pyparsing import *

identifier = Word(alphas, alphanums + '_')
number = Word(nums + ".")
assignmentExpr = identifier + "=" + (identifier | number)
assignmentTokens = assignmentExpr.parseString("pi=3.14159")
print assignmentTokens

