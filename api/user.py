#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-25
# e-mail: jwfy0902@foxmail.com

from base import *

class user(WebRequest):
    _logging = SpuLogging(module_name="user", class_name="user")

    def __init__(self):
        pass

    def login(self):
        """
        登录首页
        """
        # TODO 登录首页
        pass

    def deal_login(self, 
        username={'atype':str, 'adef':''},
        password={'atype':str, 'adef':''},
        encrypt={'atype':str, 'adef':''}
        ):
        """
        处理登录
        """
        # TODO 处理登录
        pass

    def logout(self):
        """
        退出登录
        """
        pass

    def register(self,):
        pass
