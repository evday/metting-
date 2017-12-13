#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-13,9:25"


class Base(object):
    def __init__(self,val):
        self.val = val

    def func(self):
        self.test()
        print(self.val)

    def test(self):
        print("Base")


class Foo(Base):



    def test(self):
        print("foo")

class Bar(object):

    def __init__(self):
        self._register = {}

    def register(self,a,b = None):
        if not b:
            b = Base
        self._register[a] = b(a)
b = Bar()
b.register(1,Foo)#a 就是1 b Foo()实例化的一个对象
b.register(2)#a 是1 b是Base()实例化的一个对象
b._register[1].func()
b._register[2].func()



