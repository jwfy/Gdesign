#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-25
# e-mail: jwfy0902@foxmail.com

import sys
from config import *
from sputnik.SpuLogging import SpuLogging
from sputnik.SpuError import SpuErrorCodeGen, SpuError
from sputnik.SpuUOM import setdoc

__code_gen = None

def code():
    """
    自动生成的错误码，200-1100
    """
    global __code_gen
    if not __code_gen:
        __code_gen = SpuErrorCodeGen(1000)
    return __code_gen.code()

class Error(object):
    code_dict = {}
    doc_info = ""

    @classmethod
    def load_code_tuple(cls, c='<br>'):
        for e in cls.__dict__:
            v = cls.__dict__.get(e)
            if type(v) == tuple and type(v[0]) == int and type(v[1]) == str:
                cls.code_dict[v[0]] = v
                cls.doc_info += "Msg:%s%s Code:%s%s Info:%s%s" %(e, c, v[0], c, v[1], c*2)


Error.success = (code(), "成功")
Error.fail = (code(), "未知错误")
Error.login_error = (code(), "登录失败")
Error.unlogin = (code(), "用户未登录")
Error.register_duplicate = (code(), "重复注册")
Error.register_failure = (code(), "注册失败")
Error.load_code_tuple()

info = "Error Info:<br> %s" %Error.doc_info

setdoc(info)
