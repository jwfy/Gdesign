#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-25
# e-mail: jwfy0902@foxmail.com

from config import *
from sputnik.SpuRequest import SpuRequestHandler, SpuBaseHandler
from sputnik.SpuLogging import SpuLogging
from sputnik.SpuUOM import POST, POST_FILE, UOM_WRAPS
import json


class WebRequest(SpuRequestHandler):
    """
    所有的url请求的基类
    """
    def __init__(self):
        SpuRequestHandler.__init__(self)
    
    def _get_user_session(self):
        session = self.session
        if not session:
            return None
        user_id = self.session.get("user_id", 0)
        return user_id

    def _set_user_session(self, username):
        session = self.session
        if not session:
            return None
        self.session["user_id"] = username

    def _remote_ip(self):
        return self.tornado.request.remote_ip

    def _redirect(self, uri):
        return self.tornado.redirect(uri)

    def _return_ans(self, status, message, type, kwargs):
        ans = {}
        ans["status"] = status
        ans["query"] = message
        ans["source"] = type
        for k, v in kwargs.iteritems():
            ans[k] = v
        return ans

def check_login(permission=1):
    def wrap(func):
        @UOM_WRAPS(func)
        def f(self, *args, **kwargs):
            user_name = self._get_user_session()
            if not user_name:
                self._logging.warn("未登录，请先登录")
                return self._redirect("/user/user/login")
            return func(self, *args, **kwargs)
        return f
    return wrap
