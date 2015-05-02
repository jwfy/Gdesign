#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-13
# e-mail: jwfy0902@foxmail.com

from base import *
from module.movie_ctrl import MovieCtrl
from module.recomment_ctrl import MovieReCommentCtrl
from module.image_ctrl import *

movie_ctrl = MovieCtrl(mongo_dbcnf)
removie_ctrl = MovieReCommentCtrl()

API_TOKEN = "dm_movie"

class movie(WebRequest):
    _logging = SpuLogging(module_name="movie", class_name="movie")

    def __init__(self):
        """
        前台,电影
        """
        pass

    def index(self):
        """
        首页，推荐展示的电影
        """
        ans = {}
        try:
            total, desc = removie_ctrl.list(page_size=5, status=1)
            if not total:
                r_status = "failure"
                query = desc
            else:
                r_status = "success"
                query = []
                for d in desc:
                    query_dict = {}
                    query_dict["img"] = d.img_url
                    query_dict["_id"] = d._id
                    query_dict["title"] = d.title
                    query_dict["movie"] = movie_ctrl.get(_id=d._id)
                    query.append(query_dict)
            ans = self._return_ans(r_status, query, "recommentmovie_list")
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", "", "recommentmovie_list")
        return self._html_render("index.html", ans)

    @POST
    def list(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10},
            #q={"atype": unicode, "adef":""},
            #csrf_code={"atype":str, "adef":""},
            api_type={"atype":str, "adef":""},
            token={"atype":str, "adef":""}
        ):
        """
        获取列表，通过上述条件进行筛选,前端展示
        """
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), source="list")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("front_movie.html", ans)

    @POST
    def category(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            category={"atype":unicode, "adef":""},
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过类目筛选数据
        """
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), category=category, source="category")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("front_movie.html", ans)
    
    @POST
    def year(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            year={"atype":int, "adef":0},
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过类目筛选数据
        """
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), year=int(year), source="year")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("front_movie.html", ans)
   
    @POST
    def search(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10},
            q={"atype":unicode, "adef":""},
        ):
        """
        搜索
        """
        ans = {}
        if not q:
            self._logging.warn("没有输入有效搜索内容")
            return self.tornado.redirect("/movie/movie/list")
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), q=q, source="search")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        return self._html_render("front_movie.html", ans)

    @POST
    def directors(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            directors={"atype":unicode, "adef":""},
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过导演进行搜索
        """
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), directors=directors, source="directors")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("front_movie.html", ans)

    @POST
    def casts(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            casts={"atype":unicode, "adef":""},
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过演员进行搜索
        """
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), casts=casts, source="casts")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("front_movie.html", ans)
    
    @POST
    def countries(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10}, 
            countries={"atype":unicode, "adef":""},
            api_type={"atype":str, "adef":""}, 
            token={"atype":str, "adef":""}
        ):
        """
        通过地区进行搜索
        """
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), countries=countries, source="countries")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("front_movie.html", ans)
    
    def subject(self,id={"atype":str, "adef":""},
            status={"atype":str, "adef":"online"},
            api_type={"atype":str, "adef":""},
            token={"atype":str, "adef":""}
        ):
        """
        获取 单部电影和相关数据
        """
        res =  movie_ctrl.get(_id=id, status=status)
        ans = {}
        if not res:
            self._logging.warn("没有电影信息"+id)
            ans = self._return_ans("failure", "暂无数据","subject")
        else:
            ans = self._return_ans("success", "成功获取数据","subject", 
                    dict(length=1, contains=res))
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("single.html", ans)

    def p404(self):
        return self._html_render("404.html", {})

    def p500(self):
        return self._html_render("500.html", {})
