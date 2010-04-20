#!/usr/bin/env python
# encoding: utf-8
"""
test_jsparser.py

Created by Austin Jan on 2009-11-18.
Copyright (c) 2009 AnDream. All rights reserved.
"""
import javascrip_parser as js
import unittest



class test_jsparser(unittest.TestCase):
  def setUp(self):
    pass
    
    
  def test_Keyword(self):
    assert js.isKeyword('if') == True
    assert js.isKeyword('hi') == False
    
  def test_variable(self):
    obj = js.veriable_literal()
    obj.parseString('rt4',parseAll=True)

    
  def nntest_object(self):
    simple_object = "a = {'one':'value_1','two':'value_2'}"
    obj           = js.JsObject(simple_object)
    assert obj.content[0] == "'one':'value_1'"
    
if __name__ == '__main__':
  unittest.main()
