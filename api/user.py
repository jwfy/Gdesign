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
        return self._html_render("login.html", {})

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
        if not q or q!= "dm":
            ans = self._return_ans("error", "非法登录", "user")
            self._logging.error("非法登录")
            return self._write(ans)
        try:
            r, desc = user_ctrl.deal_login(name=username, password=password)
            if not r:
                r_status = "failure"
            else:
                self._set_user_session(desc)
                desc = "登录成功"
                r_status = "success"
        except Exception as e:
            self._logging.error(e)
            r_status = "error"
            desc = e
        ans = self._return_ans(r_status, desc, "user_register")
        return self._write(ans)

    @check_login()
    def logout(self):
        """
        退出登录
        """
        ans = {}
        user = self._get_user_session()
        if not user[0]:
            ans = self._return_ans("error", "退出用户没session", "user")
            self._logging.error("非法退出")
            return self._write(ans)
        self._set_user_session()
        r, desc = user_ctrl.deal_logout(id=int(user[0]))
        return self._redirect("/user/user/login")

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

    @POST
    def update_password(self, name={"atype":unicode, "adef":""}, 
            old_password={"atype":str, "adef":""}, 
            new_password={"atype":str, "adef":""}
        ):
        """
        重置密码
        """
        pass

    @check_login()
    @POST
    def update_status(self, id={"atype":int, "adef":0}, 
            status={"atype":int, "adef":0}
        ):
        """
        更新用户状态
        """
        pass

