#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-15
# e-mail: jwfy0902@foxmail.com

from base import *
from module.comment_ctrl import CommentCtrl

comment_ctrl = CommentCtrl()

class comment(WebRequest):
    _logging = SpuLogging(module_name="comment", class_name="comment")
    
    """
    NOTICE :关于状态的值说明
    0     所有的评论均显示(仅限后台查看)
    1     评论正常显示
    2     评论被隐藏，只可以在后台显示
    3     评论被删除（虚拟删除），可以在后台恢复
    """
    
    def __init__(self):
        pass

    @POST
    def add(self, name={"atype":unicode, "adef":""},
            email={"atype":str, "adef":""}, 
            title={"atype":unicode, "adef":""}, 
            contain={"atype":unicode, "adef":""}, 
            category={"atype":str, "adef":"movie"}, 
            captcha={"atype":str, "adef":""},
            source={"atype":int, "adef":""},
            _id={"atype":str, "adef":"0"}
        ):
        """
        添加评论,_id 为 mongo _id
        source 为提交评论的来源
        注： 如果为1 表示来自 前台 提交
             否则是来自 后台 提交
        """
        if source:
            session_captcha = self._get_captcha_session()
            if not session_captcha == captcha:
                ans = self._return_ans("error", "验证码错误", "comment_add")
                return self._write(ans)

        ip = self._remote_ip()
        ans = {}
        try:
            r, desc = comment_ctrl.add(name=name, email=email, title=title, 
                    contain=contain, category=category, ip=ip, _id=_id)
            other_desc = "comment_add"
            if not r:
                r_status = "failure"
                query = desc
            else:
                r_status = "success"
                query={}
                query["time"] = desc.time.strftime("%Y-%m-%d %H:%M:%S")
                query["id"] = desc.id
                query["contain"] = desc.contain
                query["email"] = desc.email
                query["name"] = desc.name
                query["title"] = desc.title
                query["_id"] = desc._id
                other_desc = "comment_add_by_backend"
            ans = self._return_ans(r_status, query, other_desc)
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "comment_add")
        return self._write(ans)
    
    @check_login()
    @POST
    def list(self, page_num={"atype":int, "adef":1},
            page_size={"atype":int, "adef":20},
            category={"atype":str, "adef":"movie"},
            status={"atype":int, "adef":0},
            contain={"atype":unicode, "adef":""},
        ):
        """
        可以正常显示评论列表，可以提供搜索功能
        """
        ans = {}
        try:
            total, desc = comment_ctrl.list(page_num=int(page_num), 
                page_size=int(page_size), category=category, status=int(status),
                contain=contain)
            kwargs = {}
            kwargs["category"] = category
            kwargs['contain'] = contain
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
                kwargs['page_total'] = total / int(page_size) if not total % int(page_size) else total / int(page_size) + 1
            ans = self._return_ans(status, query, "comment_list", kwargs)
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "comment_list")
        return self._html_render("comment.html", ans)

    @check_login()
    @POST
    def update_status(self, ids={"atype":str, "adef":""},
            status={"atype":int, "adef":""}
        ):
        """
        更新状态,可进行批量更新
        """
        ans = {}
        ids = json.loads(ids)
        try:
            r, desc = comment_ctrl.update_status(ids=ids, status=int(status))
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
            ans = self._return_ans(r_status, desc, "comment_update_status")
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "comment_update_status")
        return self._write(ans)
