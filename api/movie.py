#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-13
# e-mail: jwfy0902@foxmail.com

from base import *
from module.movie_ctrl import MovieCtrl

movie_ctrl = MovieCtrl(mongo_dbcnf)

API_TOKEN = "dm_movie"

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
    
    def list(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过类目筛选数据
        """
        res = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size))
        ans = {}
        if not res:
            ans = self._return_ans("failure", "暂无数据","list")
        else:
            ans = self._return_ans("success", "成功获取数据","list", 
                    length=len(res), contains=res)
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._write(ans)
    
    def category(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            name={"atype":unicode, "adef":""}, 
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过类目筛选数据
        """
        res = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size), 
                category=name)
        ans = {}
        if not res:
            ans = self._return_ans("failure", "暂无数据","category")
        else:
            ans = self._return_ans("success", "成功获取数据","category", 
                    length=len(res), contains=res)
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._write(ans)
            
    def search(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, q={"atype":unicode, "adef":""}, 
            csrf_code={"atype":str, "adef":""}
        ):
        """
        搜索
        """
        ans = {}
        if csrf_code != "1234":
            self._logging.error("非法查询操作")
            ans = self._return_ans("error", "非法查询","search")
            return self._write(ans)
        if not q:
            return self._write("首页")
            # TODO 这里需要跳转到新的列表页面
        res = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size),
                q=q)
        if not res:
            ans = self._return_ans("failure", "暂无数据","search")
        else:
            ans = self._return_ans("success", "成功获取数据","search", 
                    length=len(res), contains=res)
        return self._write(ans)

    def director(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            name={"atype":unicode, "adef":""}, 
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过导演进行搜索
        """
        res = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size),
                directors=name)
        ans = {}
        if not res:
            ans = self._return_ans("failure", "暂无数据","director")
        else:
            ans = self._return_ans("success", "成功获取数据","director", 
                    length=len(res), contains=res)
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._write(ans)

    def casts(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            name={"atype":unicode, "adef":""}, 
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过导演进行搜索
        """
        res = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size),
                casts=name)
        ans = {}
        if not res:
            ans = self._return_ans("failure", "暂无数据","casts")
        else:
            ans = self._return_ans("success", "成功获取数据","casts", 
                    length=len(res), contains=res)
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._write(ans)

    def subject(self,id={"atype":str, "adef":""},
            api_type={"atype":str, "adef":""},
            token={"atype":str, "adef":""}
        ):
        """
        获取 单部电影和相关数据
        """
        movie =  movie_ctrl.get(id)
        ans = {}
        if not movie:
            self._logging.error("没有电影信息"+id)
            ans["status"] = "failure"
            ans["message"] = "没有具体的电影"
            ans = self._return_ans("failure", "暂无数据","subject")
        else:
            ans = self._return_ans("success", "成功获取数据","subject", 
                    length=1, contains=res)
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._write(ans)
