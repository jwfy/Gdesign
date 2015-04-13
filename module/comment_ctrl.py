#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-13
# e-mail: jwfy0902@foxmail.com

from sputnik.SpuLogging import SpuLogging
from sputnik.SpuDBObject import Sort, SqlNone, PageInfo, FuzzyLike, FN
from datetime import datetime
from model.comment_model import Comment
from base_ctrl import *

class CommentCtrl(Object):
    _logging = SpuLogging(moduel_name="comment_ctrl", class_name="CommentCtrl")

    def __init__(self):
        pass

    def update_status(self, id, status):
        """
        更新评论状态
        1: 评论正常显示
        2：评论被删除
        3：评论被屏蔽
        """
        comment_model = Comment.object()
        comment_t = Comment.table()
        cond = comment_t.id == id
        if not comment_model.find(cond):
            self._logging.error("更新评论状态，未找到对应评论")
            return None
        comment_model.status = status
        comment_model.update()
        return 1

    def get(self, category="movie", _id="0", status=1):
        """
        获取一个具体的博客或者电影的评论列表
        """
        comment_model = Comment.objectlist()
        comment_t = Comment.table()
        cond = comment_t.category == category
        cond &= comment_t._id == _id
        cond &= comment_t.status == status
        sort_style = Sort([(comment_t.id, Sort.desc)])
        comment_model.sort(sort_style)
        if not comment_model.find(cond):
            self._logging.error("未找到对应评论")
            return None
        comment_list = []
        for comment in comment_model:
            comment_dict = {}
            comment_dict["name"] = comment.name
            comment_dict["contain"] = comment.contain
            comment_dict["time"] = comment.time
            comment_list.append(comment_dict)
        return comment_list

    def list(self, page_num=1, page_size=10, category="movie", status=1,
            contain=""):
        """
        后台，显示评论列表
        """
        comment_model = Comment.objectlist()
        comment_t = Comment.table()
        cond = comment_t.category == category
        cond &= comment_t.status == status
        if contain:
            cond &= FuzzyLike(comment_t.contain == contain)
        pageinfo = PageInfo(page_num, page_size)
        sort_style = Sort([(comment_t.id, Sort.desc)])
        comment_model.sort(sort_style)
        comment_model.pageinfo(pageinfo)
        if not comment_model.find(cond):
            self._logging.error("未找到评论列表")
            return None
        return comment_model

    def add(self, name, email, title, contain, category="movie",ip="127.0.0.1"
            _id="0"):
        """
        添加评论,默认的显示正常
        """
        comment_model = Comment.object()
        comment_model.name = name
        comment.email = email
        comment.title = title
        comment.contain = contain
        comment.category = category
        comment.ip = ip
        comment._id = _id
        comment.status = 1
        comment.time = datetime.now()
        try:
            comment_model.insert()
            return None
        except Exception as e:
            self._logging.error(e)
            return e
            # 把错误信息返回给调用的地方,便于前端的异步调取
