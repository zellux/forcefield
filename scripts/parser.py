# -*- coding: utf-8 -*-
#!/usr/bin/python

from pyparsing import *

keywords = """
SET RETURN IF THEN ELSE WRITE_LOG FUNC
""".split()

tok_literal_set = Keyword("SET", caseless=False)
tok_literal_return = Keyword("RETURN", caseless=False)
tok_identifier = Word(alphanums + "_.-")

quoted_string = dblQuotedString
# quoted_string.setParseAction(lambda x: print(x))

expression = Word(nums) | quoted_string

statement = Forward()
set_stmt = tok_literal_set + tok_identifier.setResultsName('lhs') + '=' + expression.setResultsName('rhs')
return_stmt = tok_literal_return + expression.setResultsName('retval')
statement = Group(Or([set_stmt, return_stmt]))
statements = OneOrMore(statement)

if __name__ == '__main__':
    input = open('regression/level1.input', 'r').read()
    print input
    stats = statements.parseString(input)
    print(stats.dump())
