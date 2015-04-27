#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-27 
# e-mail: jwfy0902@foxmail.com

"""
前台页面的模块 wetget
"""

import tornado
from base import *
from module.movie_ctrl import MovieCtrl
from module.comment_ctrl import CommentCtrl

movie_ctrl = MovieCtrl(mongo_dbcnf)
comment_ctrl = CommentCtrl()

class Hot(tornado.web.UIModule):
    def render(self):
        """
        点击率分组
        """
        res = movie_ctrl.pv()
        return self.render_string('module/hot.html', res=res).strip()

class Year(tornado.web.UIModule):
    def render(self):
        """
        时间分组查询
        """
        res = movie_ctrl.year()
        return self.render_string('module/year.html', res=res).strip()

class Comment(tornado.web.UIModule):
    def render(self):
        """
        时间分组查询
        """
        res = comment_ctrl.new()
        return self.render_string('module/comment.html', res=res).strip()
