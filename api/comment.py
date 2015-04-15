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
    NOTICE :
    关于状态的值说明
    0     所有的评论均显示(仅限后台查看)
    1     评论正常显示
    2     评论被隐藏，只可以在后台显示
    3     评论被删除（虚拟删除），可以在后台恢复
    """
    
    def __init__(self):
        pass

    @POST
    def add(self, name={"atype":unicode, "adef":""},
            email={"atype":str, "adef":""}, title={"atype":unicode, "adef":""}, 
            contain={"atype":unicode, "adef":""}, category={"atype":str, "adef":"movie"}, 
            ip={"atype":str, "adef":"127.0.0.1"},
            _id={"atype":str, "adef":"0"}
        ):
        """
        添加评论
        NOTICE _id 为豆瓣id，而不是mongo 的_id
        """
        ans = {}
        try:
            r, desc = comment_ctrl.add(name=name, email=email, title=tile, 
                    contain=contain, category=category, ip=ip, _id=_id)
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
            ans = self._return_ans(r_status, desc, "comment_add")
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "comment_add")
        return self._write(ans)

    @check_login()
    @POST
    def list(self, page_num={"atype":int, "adef":1},
            page_size={"atype":int, "adef":10},
            category={"atype":str, "adef":"movie"},
            status={"atype":int, "adef":0},
            contain={"atype":unicode, "adef":""}
        ):
        """
        可以正常显示评论列表，可以提供搜索功能
        """
        ans = {}
        try:
            r, desc = comment_ctrl.list(page_num=int(page_num), 
                page_size=int(page_size), category=category, status=int(status),
                contain=contain)
            # TODO unicode 
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
            ans = self._return_ans(r_status, desc, "comment_add")
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "comment_add")
        return self._write(ans)

    @check_login()
    @POST
    def update_status(self):
        # TODO 明天写吧！！！！差不多了
        pass
