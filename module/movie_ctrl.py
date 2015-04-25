#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-11
# e-mail: jwfy0902@foxmail.com

from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from sputnik.SpuLogging import SpuLogging
from script.douban_movie_api import *
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

class MovieCtrl(object):
    _logging = SpuLogging(module_name="movie_ctrl", class_name="MovieCtrl")


    def __init__(self, mongo):
        client = MongoClient(mongo["host"], mongo["port"])
        database = client[mongo["database"]]
        self.collection = ""
        if not self.collection:
            self.collection = database[COLLECTION]  


    def list(self, page_num=1, page_size=10, status="online", q="", **kwargs):
        """
        筛选数据,获取数据列表
        NOTICE ：电影 默认 显示上线的
        """
        query = {}
        for k,v in kwargs.iteritems():
            if isinstance(v, unicode):
                query[k] = unicode_to_str(v)
            elif v:
                query[k] = str(v)
        if status:
            query["r_status"] = status
        # TODO q 模糊查询summary
        #if q:
        #    Pattern pattern = Pattern.compile("^.*" + q + ".*$")
        #    query["summary"] = pattern
        res = self.collection.find(query).limit(page_size) \
                .skip((page_num-1)*page_size).sort([("id", DESCENDING)])
        if not res.count():
            return 0, "没有数据"
        ans = []
        for r in res:
            ff = r
            _id = str(r["_id"])
            r["comment_num"] = comment_ctrl.get(_id=_id, get_num=True) or 0
            r["_id"] = str(r["_id"])
            t = r.get("down_link", "[]")
            down_num = len(list(r.get("down_link",[])))
            r.pop("down_link", "")
            r["down_num"] = down_num
            r["category"] = [unicode_to_str(ca) for ca in r["category"]]
            ans.append(r)
        return res.count(), ans

    def get(self, _id="", status="online"):
        """
        通过 _id 获取 对应的电影内容和对应评论,并且通过_id 获取对应评论
        """
        res = self.collection.find_one({"_id":ObjectId(_id), "status":status})
        if not res:
            return ""
        self.collection.update({"_id":ObjectId(_id)},{"$inc":{"pv":1}})
        _id = res["_id"]
        res["_id"] = str(_id)
        res['comment'] = comment_ctrl.get(_id=_id)
        return res

    def update_status(self, _ids=[], status=""):
        """
        更新电影的上线、下线状态
        可进行批量操作
        """
        if not _ids:
            return 0, "没有需要修改的_id值"
        if not status:
            return 0, "没有设置更新状态"
        for _id in _ids:
            _id = ObjectId(_id)
            try:
                self.collection.update({"_id":_id}, {"$set":{"status":status}})
            except Exception as e:
                self._logging.error(e)
                return 0, e
        return 1,"更新状态成功"

    def update(self, _id="", **kwargs):
        """
        更新电影具体的信息
        """
        if not _id:
            self._logging.error("更新数据失败--没有此数据")
            return 0, "无数据"
        for k,v in kwargs:
            # TODO 这里需要对格式进行检测
            query[k] = v
        try:
            self.collection.update({"_id":ObjectId(_id)}, {"$set":query})
            return 1, "更新数据成功"
        except Exception as e:
            self._logging.error(e)
            return 0, e
    
    def add(self, ids=""):
        """
        添加电影数据
        ids 应该为一序列的豆瓣 id 的值
        """
        if not _ids:
            self._logging.error("无有效id")
            return 0, "无有效id"
        _ids = []
        for id in ids:
            try:
                _id, flag = write_to_mongo(id)
                _ids.append(_id)
            except Exception as e:
                self._logging.error(e)
                pass
        if _ids:
            return _ids
        return None
