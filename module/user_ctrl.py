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
        """
        NOTICE 关于用户状态和权限的说明
        status: 
                -1 表示显示所有用户
                0 表示账户被拉黑，禁止操作
                1 表示注册，未审核(不可用)
                2 表示审核未通过，（不可用）
                10 表示账户可用
        permission： 
                    -1 显示所有权限的用户
                     0 未通过审核和未审核用户权限
                     1 只可以浏览
                     2 可用添加操作
                     3 可用修改操作
                     4 可用删除操作
                     5 可用非root权限（不可访问用户页面）
                     10 root 权限
        """
        pass

    def _password_encrypt(self, password):
        return md5("dm_account" + md5(password) + "jwfy" + md5("2015year"))

    def deal_login(self, name, password):
        """
        处理登录
        """
        user_model = User.object()
        user_t = User.table()
        cond = user_t.name == unicode_to_str(name)
        password = self._password_encrypt(password)
        cond & (user_t.password == password)
        if not user_model.find(cond):
            self._logging.error("用户名和密码不匹配")
            return 0, "用户名或者密码错误"
        user_model.login_time = datetime.now()
        user_model.update()
        return 1, (user_model.id, user_model.status, user_model.permission)
        # 返回了 用户id和用户状态，用户权限

    def deal_logout(self, id):
        """
        退出登录
        """
        user_model = User.object()
        user_t = User.table()
        cond = user_t.id == id
        if not user_model.find(cond):
            self._logging.error("退出失败")
            return 0, "退出失败"
        return 1, "退出成功"

    def reset_password(self, name="", old_password="", new_password="", id=0):
        """
        密码重置
        """
        user_model = User.object()
        user_t = User.table()
        cond = SqlNone()
        if id:
            # 如果是通过id的画则可以从后台重置用户密码
            # 重置的密码默认初始密码是dm2015
            cond = user_t.id == int(id)
            new_password = "dm2015"
            error = "不存在此用户id"
        else:
            old_password = self._password_encrypt(old_password)
            cond = user_t.name == unicode_to_str(name)
            cond & (user_t.password == old_password)
            error = "用户名和原始密码不匹配"
        if not user_model.find(cond):
            self._logging.error(error)
            return 0, error
        new_password = self._password_encrypt(new_password)
        user_model.password = new_password
        user_model.update()
        return 1, "密码修改成功"

    def deal_register(self, name, email, password):
        """
        用户注册
        """
        user_model = User.object()
        user_model.name = unicode_to_str(name)
        user_model.email = email
        password = self._password_encrypt(password)
        user_model.password = password
        user_model.register_time = datetime.now() 
        user_model.status = 1
        user_model.permission = 0
        try:
            flag = user_model.insert()
            if flag > 0:
                return 1, "用户注册成功"
            return 0, "注册失败"
        except Exception as e:
            self._logging.error(e)
            return 0, e

    def get_user(self, single=0, **kwargs):
        """
        根据相关参数，获取对应的用户信息
        如果single为1则表示获取一个用户的信息
        否则就是用户列表
        TODO 如果为用户列表，则需要添加页面和页面个数
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
            return 0, "无法获取该用户信息"
        if single:
            return -1, user_model[0]
        return 1, user_model

    def list(self, page_num=1, page_size=10, q=""):
        """
        后台，显示用户列表
        """
        user_model = User.objectlist()
        user_t = User.table()
        cond = SqlNone()
        if q:
            q = unicode_to_str(q)
            cond = (user_t.name == q)
            cond |= (user_t.email == q)
        pageinfo = PageInfo(page_num, page_size)
        sort_style = Sort([(user_t.id, Sort.desc)])
        user_model.sort(sort_style)
        user_model.pageinfo(pageinfo)
        if not user_model.find(cond):
            self._logging.warn("未找到用户列表")
            return 0, "未找到用户信息"
        sum = pageinfo.total_record
        return sum, user_model

    def update(self, id=0, kwargs={}):
        """
        更细用户数据
        """
        user_model = User.object()
        user_t = User.table()
        cond = user_t.id == int(id)
        if not user_model.find(cond):
            self._logging.warn("未找到该用户")
            return 0, "未找到该用户"
        if not kwargs:
            return 0, "无更新内容"
        for k, v in kwargs.iteritems():
            v = unicode_to_str(v) if isinstance(v, unicode) else int(v)
            setattr(user_model, k, v)
        user_model.update()
        return 1, "更新用户信息成功"

