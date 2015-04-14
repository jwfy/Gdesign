#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-10
# e-mail: jwfy0902@foxmail.com

from sputnik.SpuLogging import SpuLogging
from sputnik.SpuDBObject import Sort, SqlNone, PageInfo
from sputnik.SpuUtil import md5
from datetime import datetime
from model.user_model import User
from base_ctrl import *

class UserCtrl(object):
    _logging = SpuLogging(module_name="user_ctrl", class_name="UserCtrl")

    def __init__(self):
        pass

    def _password_encrypt(self, password):
        return md5("dm_account" + md5(password) + "jwfy" + md5("2015year"))

    def deal_login(self, name, password):
        """
        处理登录
        """
        user_model = User.object()
        user_t = User.table()
        cond = user_t.name == name
        password = self._password_encrype(password)
        cond & (user_t.password == password)
        if not user_model.find(cond):
            self._logging.error("用户名和密码不匹配")
            return None
        if user_model.status < 9:
            # TODO 需要具体化状态和等级范围和值
            self._logging.warn("用户状态不符合要求")
            return None
        user_model.login_time = datetime.now()
        user_model.update()
        return user_model.id, name

    def deal_logout(self, name):
        """
        退出登录
        """
        user_model = User.object()
        user_t = User.table()
        cond = user_t.name == name
        if not user_model.find(cond):
            return None
        return 1

    def reset_password(self, name, old_password, new_password):
        """
        密码重置
        """
        user_model = User.object()
        user_t = User.table()
        old_password = self._password_encrype(old_password)
        cond = user_t.name == name
        cond & (user_t.password == old_password)
        if not user_model.find(cond):
            self._logging.error("用户名和原始密码不匹配")
            return None
        new_password = self._password_encrype(new_password)
        user_model.password = new_password
        user_model.update()
        return 1

    def deal_register(self, name, email, password):
        """
        用户注册
        """
        user_model = User.object()
        user_model.name = name
        user_model.email = email
        password = self._password_encrype(password)
        user_model.password = password
        try:
            flag = user_model.insert()
            if flag > 0:
                return 1
            return 0
        except Exception as e:
            self._logging.error(e)
            return 0

    def get_user(self, single=0, **kwargs):
        """
        根据相关参数，获取对应的用户信息
        如果single为1则表示获取一个用户的信息
        否则就是用户列表
        """
        user_model = User.objectlist()
        user_t = User.table()
        cond = SqlNone()
        for k,v in kwargs.items():
            if v and k != "password":
                try:
                    cond = cond & (getattr(user_t, k) == v)
                except Exception as e:
                    self._logging.error(e)
        if not user_model.find(cond):
            self._logging.error("无法获取该用户信息")
            return None
        if single:
            return user_model[0]
        return user_model
