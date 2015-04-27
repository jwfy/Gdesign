#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-11
# e-mail: jwfy0902@foxmail.com

from bson import ObjectId
from bson.son import SON
from pymongo import MongoClient, ASCENDING, DESCENDING
from sputnik.SpuLogging import SpuLogging
from script.douban_movie_api import *
from base_ctrl import *
from comment_ctrl import *
import json
from datetime import datetime
import random

"""
整个的电影搜索相关的ctrl都在这里控制者
关于聚合排序索引[docs]: http://api.mongodb.org/python/current/examples/aggregation.html
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

    def year(self, ):
        """
        按照时间年限group by year
        """
        res = self.collection.aggregate([{"$group":{"_id":"$year", "count":{"$sum":1}}},{"$sort":SON([("_id",-1)])}])
        return list(res)

    def pv(self,num=10):
        """
        按照点击率多少获取前 num 个电影数据
        NOTICE ：need 字段为从mongo中筛选出来的字段
        """
        need = {"_id":1,"title":1,"pv":1}
        res = self.collection.find({}, need).limit(num).sort([("pv",-1)])
        query = []
        for r in res:
            q_dict = {}
            q_dict["_id"] = str(r["_id"])
            q_dict["pv"] = r["pv"]
            q_dict["title"] = r["title"]
            query.append(q_dict)
        return query

    def main(self, page_num=1, page_size=10, category="", directors="",
             casts="", countries="", year=0, status="online", q=""):
        """
        获取电影列表
        """
        ans = {}
        kwargs = {}
        kwargs["category"] = category
        kwargs["directors"] = directors
        kwargs["casts"] = casts
        kwargs["status"] = status
        kwargs["countries"]=countries
        kwargs["q"] = q

        total, desc = self.list(page_num=int(page_num), page_size=int(page_size),status=status, directors=directors,
                casts=casts, category=category, countries=countries, year=int(year), q=q)

        if not total:
            r_status = "failure"
            query = desc
        else:
            r_status = "success"
            kwargs["page_num"] = page_num
            kwargs["len"] = len(desc)
            kwargs["total_num"] = total
            kwargs["page_total"] = total / int(page_size) if not total % int(page_size) else total / int(page_size) + 1
        return r_status, desc, "list", kwargs

    def list(self, page_num=1, page_size=10, status="online", q="", **kwargs):
        """
        筛选数据,获取数据列表,模糊查找以完成
        NOTICE ：电影 默认 显示上线的
        """
        query = {}
        for k,v in kwargs.iteritems():
            if v and isinstance(v, unicode):
                query[k] = unicode_to_str(v)
            elif v:
                query[k] = str(v)
        if status:
            query["status"] = status
        if q:
            q = unicode_to_str(q) if isinstance(q , unicode) else str(q)
            or_list = [{"category":q}, {"countries":q}, {"casts":q}, {"directors":q}]
            or_list.append({"summary":{"$regex":q}})
            query["$or"] = or_list
        res = self.collection.find(query).limit(page_size) \
                .skip((page_num-1)*page_size).sort([("year", DESCENDING), ("rating.average", DESCENDING)])
        if not res.count():
            return 0, "没有数据"
        ans = []
        for r in res:
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
        _id = unicode_to_str(_id)
        res = self.collection.find_one({"_id":ObjectId(_id), "status":status})
        if not res:
            return ""
        self.collection.update({"_id":ObjectId(_id)},{"$inc":{"pv":1}})
        _id = str(res["_id"])
        res["_id"] = _id
        res['comment'] = comment_ctrl.get(_id=_id)
        return res

    def update_status(self, _ids=[], status=""):
        """
        更新电影的上线、下线状态
        可进行批量操作
        # TODO 需要进行单个的id更改操作
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
    
    def add(self, id=""):
        """
        添加电影数据
        ids 应该为一序列的豆瓣 id 的值
        """
        import ipdb
        ipdb.set_trace()
        if not id:
            self._logging.error("无有效id")
            return 0, "无有效id"
        try:
            _id, flag = write_to_mongo(id)
        except Exception as e:
            self._logging.error(e)
            _id = 0
            return 0, e
        return _id, flag
