#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-13
# e-mail: jwfy0902@foxmail.com

from base import *
from module.movie_ctrl import MovieCtrl

movie_ctrl = MovieCtrl()

class movie(WebRequest):
    _logging = SpuLogging(module_name="movie", class_name="movie")

    def __init__(self):
        pass

    def index(self):
        """
        首页，随机推荐五部电影
        """
        # TODO api 随机推荐
        pass
    
    def category(self, page_num=1, page_size=10, name=""):
        """
        通过类目筛选数据
        """
        movie_list = movie_ctrl.list(page_num=page_num, page_size=page_size)
        # TODO 测试使用
        for movie in movie_list:
            pass

    def search(self, page_num=1, page_size=10, token="", q=""):
        """
        搜索
        """
        if token != "1234":
            return None
        pass

    def subject(self,id):
        """
        获取 单部电影和相关数据
        """
        movie =  movie_ctrl.get(id)
        if not movie:
            self._logging.error("没有电影信息"+id)
            return None
        return self._html_render('movie_single.html', movie)
