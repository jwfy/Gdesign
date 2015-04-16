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
        self._set_user_session("jwfy")
        return self._write("hello world! python+tornado+sputnik+mysql+mongodb+redis+pypi")

    @POST
    def deal_login(self, 
            username={'atype':unicode, 'adef':''},
            password={'atype':str, 'adef':''},
            q={'atype':str, 'adef':''}
        ):
        """
        处理登录
        """
        ans = {}
        if not q:
            ans = self._return_ans("error", "非法登录", "user")
            self._logging.error("非法登录")
            return self._write(ans)
        r, desc = user_ctrl.deal_login(name=name, email=email, password=password)
        if not r:
            r_status = "failure"
        else:
            r_status = "success"
            self._set_user_session(desc)
        ans = self._return_ans(r_status, desc, "user_register")
        return self._write(ans)

    @check_login()
    @POST
    def logout(self):
        """
        退出登录
        """
        ans = {}
        id = self._get_user_session()
        if not id:
            ans = self._return_ans("error", "退出用户没session", "user")
            self._logging.error("非法退出")
            return self._write(ans)
        r, desc = user_ctrl.deal_logout(id=int(id))
        if not r:
            r_status = "failure"
        else:
            r_status = "success"
        ans = self._return_ans(r_status, desc, "user_register")
        return self._write(ans)

    @POST
    def register(self,name={"atype":unicode, "adef":""},
            email={"atype":str, "adef":""},
            password={"atype":str, "adef":""},
            q={"atype":str, "adef":""}
        ):
        """
        用户注册
        """
        ans = {}
        if not q:
            ans = self._return_ans("error", "非法注册", "user")
            self._logging.error("非法注册")
            return self._write(ans)
        r, desc = user_ctrl.deal_register(name=name, email=email, password=password)
        if not r:
            r_status = "failure"
        else:
            r_status = "success"
        ans = self._return_ans(r_status, desc, "user_register")
        return self._write(ans)

    @check_login()
    @POST
    def list(self):
        # TODO 最后一个函数了，分页
        pass
