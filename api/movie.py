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

#    @POST
#    def re_update_status(self, ids={"atype":str, "adef":""},
#            status={"atype":int, "adef":""}
#        ):
#        """
#        推荐电影状态更新
#        """
#        ans = {}
#        ids = json.loads(ids)
#        try:
#            r, desc = removie_ctrl.update_status(ids=ids, status=int(status))
#            if not r:
#                r_status = "failure"
#            else:
#                r_status = "success"
#            ans = self._return_ans(r_status, desc, "recommentmovie_update_status")
#        except Exception as e:
#            self._logging.error(e)
#            ans = self._return_ans("error", e, "recommentmovie_update_status")
#        return self._write(ans)
#
#    @POST
#    def re_list(self, page_num={"atype":int, "adef":1},
#            page_size={"atype":int, "adef":5},
#            status={"atype":int, "adef":0},
#            contain={"atype":unicode, "adef":""},
#        ):
#        """
#        推荐电影
#        """
#        ans = {}
#        try:
#            total, desc = removie_ctrl.list(page_num=int(page_num), 
#                page_size=int(page_size), status=int(status),
#                title=contain)
#            kwargs = {}
#            kwargs['title'] = contain
#            kwargs['r_status'] = status
#
#            if not total:
#                status = "failure"
#                query = desc
#            else:
#                status = "success"
#                query = []
#                for d in desc:
#                    field_name = d.object_field_names()
#                    query_dict = {}
#                    for field in field_name:
#                        value = getattr(d, field)
#                        query_dict[field] = value
#                    query.append(query_dict)
#                kwargs['total_num'] = total
#                kwargs['len'] = len(query)
#                kwargs['page_num'] = page_num
#                if total % int(page_size) == 0:
#                    kwargs['page_total'] = total / int(page_size)
#                else:
#                    kwargs['page_total'] = total / int(page_size) + 1
#            ans = self._return_ans(status, query, "recommentmovie_list", kwargs)
#        except Exception as e:
#            self._logging.error(e)
#            ans = self._return_ans("error", e, "recommentmovie_list")
#        return self._html_render("removie.html", ans)
#
#    @POST 
#    def re_add(self, title={"atype":unicode, "adef":""},
#            _id={"atype":str, "adef":"",}, img_url={"atype":str, "adef":""}
#        ):
#        """
#        推荐电影添加
#        _id 为 mongo _id
#        """
#        if not img_url:
#            return self._html_render("movie/add.html", {"title":title, "_id":_id})
#        try:
#            r, desc = removie_ctrl.add(title=title, _id=_id, img_url=img_url)
#            if not r:
#                r_status = "failure"
#            else:
#                r_status = "success"
#                desc = "首页推荐电影添加成功"
#            ans = self._return_ans(r_status, desc, "recommentmovie_add")
#        except Exception as e:
#            self._logging.error(e)
#            ans = self._return_ans("error", e, "recommentmovie_add")
#        return self._write(ans)
#
#    @POST
#    def m_add(self, id={"atype":str, "adef":""}
#        ):
#        """
#        添加电影数据
#        NOTICE： 通过豆瓣电影ID 获取相关数据
#        """
#        # TODO 添加电影数据
#        if not id:
#            return self._html_render("addmovie.html",{})
#        _id, desc = movie_ctrl.add(id)
#        if _id:
#            status = "success"
#            desc = _id
#        else:
#            status = "failure"
#        ans = self._return_ans(status, desc,"movie_add")
#        return self._write(ans)
#
#    @POST
#    def add(self, name={"atype":unicode, "adef":""},
#            email={"atype":str, "adef":""}, 
#            title={"atype":unicode, "adef":""}, 
#            contain={"atype":unicode, "adef":""}, 
#            category={"atype":str, "adef":"movie"}, 
#            ip={"atype":str, "adef":"127.0.0.1"},
#            captcha={"atype":str, "adef":""},
#            _id={"atype":str, "adef":"0"}
#        ):
#        """
#        添加评论,_id 为 mongo id
#        """
#        ip = self._remote_ip()
#        ans = {}
#        try:
#            r, desc = comment_ctrl.add(name=name, email=email, title=title, 
#                    contain=contain, category=category, ip=ip, _id=_id)
#            other_desc = "comment_add"
#            if not r:
#                r_status = "failure"
#                query = desc
#            else:
#                r_status = "success"
#                query={}
#                query["time"] = desc.time.strftime("%Y-%m-%d %H:%M:%S")
#                query["id"] = desc.id
#                query["contain"] = desc.contain
#                query["email"] = desc.email
#                query["name"] = desc.name
#                query["title"] = desc.title
#                query["_id"] = desc._id
#                other_desc = "comment_add_by_backend"
#            ans = self._return_ans(r_status, query, other_desc)
#        except Exception as e:
#            self._logging.error(e)
#            ans = self._return_ans("error", e, "comment_add")
#        return self._write(ans)
#    
#    #@check_login()
#    @POST
#    def m_list(self, page_num={"atype":int, "adef":1}, 
#            page_size={"atype":int, "adef":10},
#            category={"atype": unicode, "adef":""},
#            directors={"atype": unicode, "adef":""},
#            casts={"atype": unicode, "adef":""},
#            countries={"atype":unicode, "adef":""},
#            year={"atype":int, "adef":0},
#            status={"atype":str, "adef":""},
#            q={"atype": unicode, "adef":""},
#            csrf_code={"atype":str, "adef":""},
#        ):
#        """
#        获取列表，通过上述条件进行筛选
#        """
#        ans = {}
#        kwargs = {}
#        kwargs["category"] = category
#        kwargs["directors"] = directors
#        kwargs["casts"] = casts
#        kwargs["status"] = status
#        kwargs["countries"]=countries
#        kwargs["q"] = q
#        if q and csrf_code != "1234":
#            self._logging.error("非法查询操作")
#            ans = self._return_ans("error", "非法查询","search", kwargs)
#            return self._write(ans)
#        total, desc = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size),status=status, directors=directors,
#                casts=casts, category=category, countries=countries, year=int(year), q=q)
#
#        if not total:
#            r_status = "failure"
#            query = desc
#        else:
#            r_status = "success"
#
#            kwargs["page_num"] = page_num
#            kwargs["len"] = len(desc)
#            kwargs["total_num"] = total
#            kwargs["page_total"] = total / int(page_size) if not total % int(page_size) else total / int(page_size) + 1
#        ans = self._return_ans(r_status, desc,"list", kwargs)
#        return self._html_render("movie.html", ans)
    
    @POST
    def list(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10},
            q={"atype": unicode, "adef":""},
            csrf_code={"atype":str, "adef":""},
            api_type={"atype":str, "adef":""},
            token={"atype":str, "adef":""}
        ):
        """
        获取列表，通过上述条件进行筛选,前端展示
        """
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), q=q, source="list")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        if api_type == "json" and token == API_TOKEN:
            return self._write(ans)
        return self._html_render("front_movie.html", ans)

#        ans = {}
#        kwargs = {}
#        kwargs["category"] = category
#        kwargs["directors"] = directors
#        kwargs["casts"] = casts
#        kwargs["countries"] = countries
#        kwargs["year"] = year
#        kwargs["q"] = q
#        if q and csrf_code != "1234":
#            self._logging.error("非法查询操作")
#            ans = self._return_ans("error", "非法查询","search", kwargs)
#            return self._write(ans)
#        total, desc = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size), directors=directors,
#                casts=casts, category=category, countries=countries, year=int(year), q=q)
#
#        if not total:
#            r_status = "failure"
#            query = desc
#        else:
#            r_status = "success"
#
#            kwargs["page_num"] = page_num
#            kwargs["len"] = len(desc)
#            kwargs["total_num"] = total
#            kwargs["page_total"] = total / int(page_size) if not total % int(page_size) else total / int(page_size) + 1
#        ans = self._return_ans(r_status, desc,"list", kwargs)
#        if api_type == "json" and token == API_TOKEN:
#            return self._write(ans)
#        return self._html_render("front_movie.html", ans)
   
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
            self._logging.warn("没有输入有效搜索内容")
            return self.tornado.redirect("/movie/movie/list")
        ans = movie_ctrl.main(page_num=int(page_num), page_size=int(page_size), q=q, source="list")
        ans = self._return_ans(ans[0], ans[1], ans[2], ans[3])
        return self._html_render("front_movie.html", ans)

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
    
    def about(self):
        return self._html_render("about.html", {})

    @check_login()
    @POST
    def update_status(self, 
            _ids={"atype":str, "adef":""},
            status={"adef":str, "adef":""}
        ):
        """
        更新电影的状态
        # TODO 将会移到main 函数中 2015-04-27 18:56:05
        """
        ans = {}
        # TODO eval 函数 应该被抛弃
        r,desc = movie_ctrl.update_status(_ids=eval(_ids), status=status)
        if not r:
            r_status = "error"
        else:
            r_status = "success"
        ans = self._return_ans(r_status, desc, "update_status")
        return self._write(ans)

    @check_login()
    @POST
    def update(self,
            _id={"atype":str, "adef":""},
            summary={"atype":unicode, "adef":""}, 
            down_link={"atype":unicode, "adef":""}
        ):
        """
        更新具体的电影信息
        NOTICE 只是提供修改下载链接和电影简介
        # TODO 也会移到main 函数中，2015-04-27 18:56:34
        """
        ans = {}
        r, desc = movie_ctrl.update(_id=_id, summary=summary, down_link=down_link)
        if not r:
            r_status = "error"
        else:
            r_status = "success"
        ans = self._return_ans(r_status, desc, "update")
        return self._write(ans)

         
        
