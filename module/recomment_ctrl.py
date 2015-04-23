#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-13
# e-mail: jwfy0902@foxmail.com

from sputnik.SpuLogging import SpuLogging
from sputnik.SpuDBObject import Sort, SqlNone, PageInfo, FuzzyLike, FN, In
from datetime import datetime
from model.recomment_model import MovieReComment
from base_ctrl import *

class MovieReCommentCtrl(object):
    _logging = SpuLogging(module_name="recomment_ctrl", class_name="MovieReCommentCtrl")

    def __init__(self):
        """
        电影推荐控制层
        """
        pass

    def update_status(self, ids, status):
        """
        更新推荐电影状态,可以进行批量操作
        1: 上线
        2：下线
        """
        recomment_model = MovieReComment.objectlist()
        recomment_t = MovieReComment.table()
        if not isinstance(ids, list):
            id = ids
            ids = []
            ids.append(int(id))
        cond = In(recomment_t.id, ids)
        if not recomment_model.find(cond):
            self._logging.error("更新电影推荐状态，未找到对应数据")
            return 0, "没有找到对应推荐信息"
        recomment_model.update({'status':status, 'update_time':datetime.now()})
        return 1, "状态更新成"

    def list(self, page_num=1, page_size=10, status=0,
            title=""):
        """
        显示电影推荐列表
        """
        recomment_model = MovieReComment.objectlist()
        recomment_t = MovieReComment.table()
        cond = SqlNone()
        if status:
            cond &= recomment_t.status == status
        if title:
            cond &= FuzzyLike(recomment_t.title, unicode_to_str(title))
        pageinfo = PageInfo(page_num, page_size)
        sort_style = Sort([(recomment_t.status, Sort.asc), (recomment_t.id, Sort.desc)])
        recomment_model.sort(sort_style)
        recomment_model.pageinfo(pageinfo)
        if not recomment_model.find(cond):
            self._logging.warn("未找到推荐列表")
            return 0, "没有推荐电影信息"
        sum = pageinfo.total_record
        return sum, recomment_model

    def add(self, title, _id, img_url):
        """
        添加电影推荐
        默认设置状态为“下线”状态
        """
        recomment = MovieReComment.object()
        recomment.title = unicode_to_str(title)
        recomment.time = datetime.now()
        recomment.update_time = datetime.now()
        comment._id = _id
        comment.status = 2
        recomment.img_url = img_url
        try:
            recomment.insert()
            return 1,recomment
        except Exception as e:
            self._logging.error(e)
            return 0, e
