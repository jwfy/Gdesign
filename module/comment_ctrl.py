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

class CommentCtrl(object):
    _logging = SpuLogging(module_name="comment_ctrl", class_name="CommentCtrl")

    def __init__(self):
        """
        评论控制层
        """
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
        cond = comment_t.id == int(id)
        if not comment_model.find(cond):
            self._logging.error("更新评论状态，未找到对应评论")
            return 0, "没有找到对应评论信息"
        comment_model.status = int(status)
        comment_model.update()
        return 1, "评论更新成"

    def get(self, category="movie", _id="0", status=1, get_num=False):
        """
        获取一个具体的博客或者电影的评论列表
        NOTICE 如果get_num 为True 则是返回其个数，否则是
        """
        comment_model = Comment.objectlist()
        comment_t = Comment.table()
        cond = comment_t.category == category
        cond &= comment_t._id == _id
        cond &= comment_t.status == status
        sort_style = Sort([(comment_t.id, Sort.desc)])
        comment_model.sort(sort_style)
        if not comment_model.find(cond):
            self._logging.warn("未找到对应评论")
            return None
        comment_list = []
        for comment in comment_model:
            comment_dict = {}
            comment_dict["name"] = comment.name
            comment_dict["contain"] = comment.contain
            comment_dict["time"] = comment.time
            comment_list.append(comment_dict)
        if get_num:
            return len(comment_list)
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
            cond &= FuzzyLike(comment_t.contain == unicode_to_str(contain))
        pageinfo = PageInfo(page_num, page_size)
        sort_style = Sort([(comment_t.id, Sort.desc)])
        comment_model.sort(sort_style)
        comment_model.pageinfo(pageinfo)
        if not comment_model.find(cond):
            self._logging.warn("未找到评论列表")
            return 0, "没有评论信息"
        sum = pageinfo.total_record
        return sum, comment_model

    def add(self, name, email, title, contain, category, ip, _id):
        """
        添加评论,默认的显示正常
        """
        comment_model = Comment.object()
        comment_model.name = unicode_to_str(name)
        comment.email = email
        comment.title = unicode_to_str(title)
        comment.contain = unicode_to_str(contain)
        comment.category = category
        comment.ip = ip
        comment._id = _id
        comment.status = 1
        comment.time = datetime.now()
        try:
            comment_model.insert()
            return 1,"添加成功"
        except Exception as e:
            self._logging.error(e)
            return 0, e
