#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-27
# e-mail: jwfy0902@foxmail.com

from base import *
from module.movie_ctrl import MovieCtrl
from module.recomment_ctrl import MovieReCommentCtrl
from module.image_ctrl import *

movie_ctrl = MovieCtrl(mongo_dbcnf)
removie_ctrl = MovieReCommentCtrl()

API_TOKEN = "dm_movie"
"""
后台主函数
"""

class movie(WebRequest):
    _logging = SpuLogging(module_name="main", class_name="movie")

    def __init__(self):
        """
        后台，电影
        """
        pass

    @POST
    def add(self, id={"atype":str, "adef":""}
        ):
        """
        添加电影数据
        NOTICE： 通过豆瓣电影ID 获取相关数据
        id格式为'********   ********* *******'
        会根据这种样式进行操作处理
        """
        if not id:
            return self._html_render("addmovie.html",{})
        ids = id.split()
        num = []
        for id in ids:
            try:
                _id, desc = movie_ctrl.add(id)
                if _id:
                    num.append(_id)
            except Exception as e:
                self._logging.error(e)
                continue
        
        if num:
            status = "success"
            desc = num
        else:
            status = "failure"
        ans = self._return_ans(status, desc,"movie_add")
        return self._write(ans)

    #@check_login()
    @POST
    def list(self, page_num={"atype":int, "adef":1},
            page_size={"atype":int, "adef":10},
            category={"atype": unicode, "adef":""},
            directors={"atype": unicode, "adef":""},
            casts={"atype": unicode, "adef":""},
            countries={"atype":unicode, "adef":""},
            year={"atype":int, "adef":0},
            status={"atype":str, "adef":""},
            q={"atype": unicode, "adef":""},
        ):
        """
        获取列表，通过上述条件进行筛选
        """
        ans = {}
        kwargs = {}
        kwargs["category"] = category
        kwargs["directors"] = directors
        kwargs["casts"] = casts
        kwargs["status"] = status
        kwargs["countries"]=countries
        kwargs["q"] = q
        total, desc = movie_ctrl.list(page_num=int(page_num), page_size=int(page_size),status=status, directors=directors,
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
        ans = self._return_ans(r_status, desc,"list", kwargs)
        return self._html_render("movie.html", ans)

    #@check_login()
    @POST
    def update_status(self,
            _ids={"atype":str, "adef":""},
            status={"adef":str, "adef":""}
        ):
        """
        更新电影的状态
        """
        ans = {}
        ids = json.loads(_ids)
        r,desc = movie_ctrl.update_status(_ids=ids, status=status)
        if not r:
            r_status = "error"
        else:
            r_status = "success"
        ans = self._return_ans(r_status, desc, "update_status")
        return self._write(ans)

    #@check_login()
    @POST
    def update(self,
            _id={"atype":str, "adef":""},
            size={"atype":str, "adef":""},
            pos={"atype":unicode, "adef":-1},
            name={"atype":unicode, "adef":""},
            url={"atype":str, "adef":""},
            source={"atype":str, "adef":""}
        ):
        """
        具体的电影信息操作
        根据source 的值 进行不同操作
        NOTICE: source 值
            "add"  添加电影下载地址
            "delete" 删除电影下载地址
            "update" 修改电影下载地址
        """
        ans = {}
        r, desc = movie_ctrl.update(_id=_id, source=source, pos=pos, size=size, 
                name=name, url=url)
        if not r:
            r_status = "error"
        else:
            r_status = "success"
        ans = self._return_ans(r_status, desc, "update")
        return self._write(ans)

    def subject(self, id={"atype":str, "adef":""}):
        """
        查看具体的电影详情
        """
        res = movie_ctrl.get(_id=id)
        ans = {}
        if not res:
            self._logging.warn("没有相关电影信息"+id)
            ans = self._return_ans("failure", "暂无数据", "subject")
        else:
            ans = self._return_ans("success", "成功获取数据", "subject", dict(contain=res))
        return self._html_render("item.html", ans)

class re(WebRequest):
    _logging = SpuLogging(module_name="main", class_name="re")

    def __init__(self):
        """
        推荐电影
        """
        pass

    @POST
    def update_status(self, ids={"atype":str, "adef":""},
            status={"atype":int, "adef":""}
        ):
        """
        推荐电影状态更新
        """
        ans = {}
        ids = json.loads(ids)
        try:
            r, desc = removie_ctrl.update_status(ids=ids, status=int(status))
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
            ans = self._return_ans(r_status, desc, "recommentmovie_update_status")
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "recommentmovie_update_status")
        return self._write(ans)

    @POST
    def list(self, page_num={"atype":int, "adef":1},
            page_size={"atype":int, "adef":5},
            status={"atype":int, "adef":0},
            contain={"atype":unicode, "adef":""},
        ):
        """
        推荐电影
        """
        ans = {}
        try:
            total, desc = removie_ctrl.list(page_num=int(page_num),
                page_size=int(page_size), status=int(status),
                title=contain)
            kwargs = {}
            kwargs['title'] = contain
            kwargs['r_status'] = status

            if not total:
                status = "failure"
                query = desc
            else:
                status = "success"
                query = []
                for d in desc:
                    field_name = d.object_field_names()
                    query_dict = {}
                    for field in field_name:
                        value = getattr(d, field)
                        query_dict[field] = value
                    query.append(query_dict)
                kwargs['total_num'] = total
                kwargs['len'] = len(query)
                kwargs['page_num'] = page_num
                if total % int(page_size) == 0:
                    kwargs['page_total'] = total / int(page_size)
                else:
                    kwargs['page_total'] = total / int(page_size) + 1
            ans = self._return_ans(status, query, "recommentmovie_list", kwargs)
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "recommentmovie_list")
        return self._html_render("removie.html", ans)

    @POST
    def add(self, title={"atype":unicode, "adef":""},
            _id={"atype":str, "adef":"",}, img_url={"atype":str, "adef":""}
        ):
        """
        推荐电影添加
        _id 为 mongo _id
        """
        if not img_url:
            return self._html_render("movie/add.html", {"title":title, "_id":_id})
        try:
            r, desc = removie_ctrl.add(title=title, _id=_id, img_url=img_url)
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
                desc = "首页推荐电影添加成功"
            ans = self._return_ans(r_status, desc, "recommentmovie_add")
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "recommentmovie_add")
        return self._write(ans)
