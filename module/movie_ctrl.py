#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-11
# e-mail: jwfy0902@foxmail.com

from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from sputnik.SpuLogging import SpuLogging
from base_ctrl import *
from comment_ctrl import *
import json
import datetime
import random

"""
整个的电影搜索相关的ctrl都在这里控制者
"""
COLLECTION = "movie"
comment_ctrl = CommentCtrl()

class MovieCtrl(Object):
    _logging = SpuLogging(module_name="movie_ctrl", class_name="MovieCtrl")


    def __init__(self, mongo):
        client = MongoClient(mongo["host"], mongo["port"])
        database = client[mongo["database"]]
        if not self.collection
            self.collection = database[COLLECTION]  

    def recommendation(self):
        """
        首页随机推荐的五部电影
        """
        # TODO 随机获取

    def list(self, page_num=1, page_size=10, q="", **kwargs):
        """
        筛选数据,获取数据列表
        """
        query = {}
        for k,v in kwargs.iteritems():
            query[k] = v
        # TODO q 模糊查询summary
        ress = self.collection.find(query).limit(page_size) \
                .skip((page_num-1)*page_size).sort("id":pymongo.DESCENDING)
        if not ress.count():
            return None
        movie_list = [res for res in ress]
        return movie_list

    def get(self, _id=""):
        """
        通过 _id 获取 对应的电影内容和对应评论
        """
        res = self.collection.find_one({"_id":_id})
        if not res.count():
            return None
        res = res[0]
        id = res.get("id", 0)
        res['comment'] = comment_ctrl.get(_id=id)
        return res
