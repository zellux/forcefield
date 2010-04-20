#!/usr/bin/env python
# encoding: utf-8
"""
javascrip_parser.py

Created by Austin Jan on 2009-11-10.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import pyparsing as lr
import os

keywords_string ="""
abstract boolean break byte case catch
char class const continue debugger
default delete do double else enum
export extends false final finally
float for function goto if implements
import in instanceof int interface long
native new null package private protected
public return short static super switch
synchronized this throw throws transient
true try typeof var void volatile while
with"""

keywords = keywords_string.split()

def veriable_literal():
  return lr.Word(lr.alphanums+'_')
  
def isKeyword(instring):
  """Check instring is javascript keyword?"""
  global keywords
  return instring in keywords
    
class JsObject(object):
  """jsObject object."""
  def __init__(self,instring):
    super(JsObject, self).__init__()
    self.ori_str = instring
    
    
class HelloParser(object):
  """Parser simple hello sentence."""
  def __init__(self):
    super(HelloParser, self).__init__()
    self.name = None
    self.initParser()
    
  def initParser(self):
    """Initialize parser"""
    words       = lr.Word(lr.alphas)
    name        = lr.Word(lr.alphas+",'")
    greet_word  = words
    names       = lr.Group(lr.OneOrMore(name))
    comma       = lr.Literal(",")
    endpunc     = lr.oneOf("! ?")
    greeting    = greet_word + comma + names.setResultsName('name') + endpunc
    self.parser = greeting
      
  def input(self,input):
    """input string will be parsed"""
    self.input = input
    result     = self.parser.parseString(input)
    print 'result : ', result.name
    self.name = ''.join(result.name)
    #self.name = resutlt.name.join('')
    
def express():
  # Supress Literal
  COLON          = lr.Suppress(":")
  LEFT_BRACKET   = lr.Suppress("{")
  RIGHT_BRACKET  = lr.Suppress("}")
  COMMA          = lr.Suppress(",")
  
  # comment
  comment = lr.cppStyleComment
  
  # bool type
  booleans = ( lr.Keyword('true') | lr.Keyword('false'))
  
  # null type
  null = lr.Keyword('null')
  
  # name
  names       = lr.Word( lr.alphas + '_' ) + \
                lr.Optional( lr.Word(lr.alphanums + '-') )
            
  #string literal -> using quotedString
  # number_literal
  integers    = ( lr.Word("123456789") + lr.Optional(lr.nums)  | "0" )
  fractions   = "." + lr.Word(lr.nums)
  exponential = (lr.Literal('e') | lr.Literal('E')) +\
                lr.Optional(( lr.Literal('+') | lr.Literal('-') )) +\
                lr.Optional(lr.Word(lr.nums))
  number_literal = integers + lr.Optional( fractions ) + lr.Optional( exponential )
  
  expression = lr.Forward()
  
  # array-literal
  array_literal = "[" + lr.Optional(expression + lr.ZeroOrMore( ","+ expression))  + "]"
  
  # object-literal
  keys = ( names | lr.quotedString )
  values = expression
  object_item    =  keys + ":" + values 
  object_literal = LEFT_BRACKET + \
                    lr.Optional(
                          object_item + 
                          lr.ZeroOrMore(","+object_item)
                          ) + \
                    RIGHT_BRACKET
                   
  
  expression << (  names
                   | null
                   | booleans
                   | number_literal 
                   | lr.quotedString 
                   | lr.Group( object_literal ) 
                   | lr.Group( array_literal ))
    
  print object_literal.parseString('{"key3": [22,"OK"]}')
  print expression.parseString('{"key":{"key":22},\n"key2":"hello"}')
  print object_literal.parseString('{"key3": [22,"OK"],"key4":4,  "key5":5}')
  print object_literal.parseString('{"key":{"key":22},\n"key2":"hello",\n"key3":[1,2,"true"]}')
  teststring = '{"g_no":"11091013034272","www_host":"http:\/\/www.ruten.com.tw","mybid_host":"http:\/\/mybid.ruten.com.tw","goods_host":"http:\/\/goods.ruten.com.tw","point_host":"http:\/\/point.ruten.com.tw","member_host":"https:\/\/member.ruten.com.tw","class_host":"http:\/\/class.ruten.com.tw","img_host":"http:\/\/img.ruten.com.tw","seller_user_nick":"ilovehome18","countdown_url":"http:\/\/mybid.ruten.com.tw\/upload\/countdown.htm?g_no=11091013034272","board_img_path":"http:\/\/img.ruten.com.tw\/board\/i\/l\/ilovehome18.570.gif?1256622520","goods_img":["s2\/1\/ad\/20\/11091013034272_925.jpg","s2\/1\/ad\/20\/11091013034272_905.jpg","s2\/1\/ad\/20\/11091013034272_427.jpg"],"refer_enced":"http%3A%2F%2Fgoods.ruten.com.tw%2Fitem%2Fshow%3F11091013034272","g_class":"0002000500110002","friend_list_overflow":"","friend_has_exists":"","bid_rid":"","ms":"uOaI6HEiffKH8YvYi\/OJ2ITtfeqGW8Hmg\/GH9W71ifNu7oPngPDsHoz7gwh75X9WtWE58Yf1bvWJ827mfeiE7YZoF2y+8Yf1bvWJ827mfemE7obxh\/Vu9YnzbuZ96nzshvGH9W71ifNu5n3pg+uG8Yf1bvWJ827mfemA5oZiu\/GH9W71ifNu6HvlfOaG1Qyv9V7JX0Nf9FmiWzLgEF0Dfcnmg+XvbclqAFst27joiOaD5XEif\/J727jqiOaD5XEigfKB27jsiOaD5XEig\/KN27juiOhxInzliOl+7YDtf+5xInzmiNu45n3yfjM3MzU=","g_mode":"B","g_direct_price":"180","goods_mail":[],"pay_mail":[],"filler_no":null,"filler_type":null,"is_nbc":false,"is_seller":0,"is_cstore":true,"use_kwa":true,"use_4ca":true},'
  print object_literal.parseString(teststring)

def run():
  """test function"""
  identifier = lr.Word( lr.alphas ) + \
               lr.Optional( lr.Word(lr.alphanums + '-') )
  numbers  = lr.Word( lr.nums + "." )
  booleans = ( lr.Keyword('true') | lr.Keyword('false'))
  
  key_           = ( identifier | numbers | lr.quotedString )
  value_         = ( lr.quotedString | numbers | booleans )
  key            = key_.setResultsName('KEY')
  value          = value_.setResultsName('VALUE')
  COLON          = lr.Suppress(":")
  LEFT_BRACKET   = lr.Suppress("{")
  RIGHT_BRACKET  = lr.Suppress("}")
  COMMA          = lr.Suppress(",")
  dict_item      = key+ COLON +value
  object_literal = LEFT_BRACKET + lr.ZeroOrMore(dict_item + COMMA ) + dict_item + RIGHT_BRACKET
  assigned       = ( object_literal | lr.quotedString | numbers | booleans )
  assigment      = lr.Optional("var") + identifier + "=" + assigned
  
  print 'Test1'
  print 'boolean("true")                 = ',booleans.parseString('true')
  print 'key("string")                   = ',key.parseString('"string"')
  print "key('','single quoted string ') = ",key.parseString("'Single quoted'")
  print 'numbers("33.23")                = ',numbers.parseString('33.23')
  print 'key(33.23)                      = ',key.parseString('33.23')
  print 'Key(int_var)                    = ',key.parseString('int_var')
  
  
  print "'key1':true       = ", dict_item.parseString("'key1':true")
  print "'key2':'two'      = ",dict_item.parseString("'key2':'two'")
  print "'key3'    :3      = ",dict_item.parseString("'key3'       :3")
  print "'key4':    'four' = ",dict_item.parseString("'key4':   'four'")
  result = dict_item.parseString("'key5':   false")
  print "'key5':false key=%s v=%s" % (result.KEY, result.VALUE)
  print object_literal.parseString('{"key1":true,\n"key2":"two"}')
 
  
def main():
  #run()
  express()


if __name__ == '__main__':
  main()

