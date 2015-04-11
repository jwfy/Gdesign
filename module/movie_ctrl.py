#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-11
# e-mail: jwfy0902@foxmail.com

from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from sputnik.SpuLogging import SpuLogging
from base_ctrl import *
import json
import datetime
import random

"""
整个的电影搜索相关的ctrl都在这里控制者
"""
COLLECTION = "movie"

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
        pass

    def list(self, page_num=1, page_size=10, q="", **kwargs):
        """
        筛选数据,获取数据列表
        """
        query = {}
        for k,v in kwargs.iteritems():
            query[k] = v
        pass
        
