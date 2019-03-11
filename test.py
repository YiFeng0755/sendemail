#!/usr/bin/python
#-*- encoding:utf-8 -*-
import sys
import chardet
str = sys.argv[1]
print (chardet.detect(str))
str = u'%s'%str
str2 ="IM\xb9\xd2\xbb\xfa\xb2\xe2\xca\xd4.html"
print (chardet.detect(str2))

if str == str2:
    print (True)

# b = repr(str)
# print unicode(eval(b),"gbk")

c = str.decode('gbk')
print (c)
d = str2.decode('gbk')
print (d)