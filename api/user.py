#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-25
# e-mail: jwfy0902@foxmail.com

from base import *
from module.user_ctrl import UserCtrl

user_ctrl = UserCtrl()

class user(WebRequest):
    _logging = SpuLogging(module_name="user", class_name="user")

    def __init__(self):
        pass

    def login(self):
        """
        登录首页
        """
        # TODO 登录首页
        self._set_user_name("jwfy")
        return self._write("hello world! python+tornado+sputnik+mysql+mongodb+redis+pypi")

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
    
    @check_login()
    def logout(self):
        """
        退出登录
        """
        ip = self._remote_ip()
        return self._write("检查session中 %s" %(ip))

    def register(self,):
        pass
