#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-25
# e-mail: jwfy0902@foxmail.com

from base import *
from module.user_ctrl import UserCtrl
from module.email_ctrl import *

user_ctrl = UserCtrl()

class user(WebRequest):
    _logging = SpuLogging(module_name="user", class_name="user")

    def __init__(self):
        pass

    def login(self):
        """
        登录首页
        """
        return self._html_render("login.html", {})

    def register(self):
        """
        注册页面
        """
        return self._html_render("user/register.html", {})
    
    def passwd(self):
        """
        修改密码页面
        """
        self._set_user_session()
        return self._html_render("user/password.html", {})
    
    @POST
    def deal_login(self, 
            username={'atype':unicode, 'adef':''},
            password={'atype':str, 'adef':''},
            q={'atype':str, 'adef':''}
        ):
        """
        处理登录
        """
        ans = {}
        if not q or q!= "dm":
            ans = self._return_ans("error", "非法登录", "user")
            self._logging.error("非法登录")
            return self._write(ans)
        try:
            r, desc = user_ctrl.deal_login(name=username, password=password)
            if not r:
                r_status = "failure"
            else:
                self._set_user_session(desc)
                desc = "登录成功"
                r_status = "success"
        except Exception as e:
            self._logging.error(e)
            r_status = "error"
            desc = e
        ans = self._return_ans(r_status, desc, "user_register")
        return self._write(ans)

    @check_login(NO_LIMIT)
    def logout(self):
        """
        退出登录
        """
        ans = {}
        user = self._get_user_session()
        if not user[0]:
            ans = self._return_ans("error", "退出用户没session", "user")
            self._logging.error("非法退出")
            return self._write(ans)
        self._set_user_session()
        r, desc = user_ctrl.deal_logout(id=int(user[0]))
        return self._redirect("/user/user/login")

    @POST
    def deal_register(self,name={"atype":unicode, "adef":""},
            email={"atype":str, "adef":""},
            password={"atype":str, "adef":""},
            q={"atype":str, "adef":""}
        ):
        """
        用户注册
        """
        ans = {}
        if not q:
            ans = self._return_ans("error", "非法注册", "user_register")
            self._logging.error("非法注册")
            return self._write(ans)
        try:
            r, desc = user_ctrl.deal_register(name=name, email=email, password=password)
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
        except Exception as e:
            r_status = "error"
            desc = e
        ans = self._return_ans(r_status, desc, "user_register")
        return self._write(ans)

    @POST
    def update_password(self, name={"atype":unicode, "adef":""}, 
            q={"atype":str, "adef":""}, 
            email={"atype":str, "adef":""}, 
            old_password={"atype":str, "adef":""}, 
            new_password={"atype":str, "adef":""}
        ):
        """
        重置密码
        """
        ans = {}
        if not q:
            ans = self._return_ans("error", "非法修改密码", "update_password")
            self._logging.error("非法修改密码")
            return self._write(ans)
        try:
            r, desc = user_ctrl.reset_password(name=name, email=email, 
                old_password=old_password, new_password=new_password)
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
        except Exception as e:
            r_status = "error"
            desc = e
        ans = self._return_ans(r_status, desc, "update_password")
        return self._write(ans)

    @check_login(UPDATE)
    @POST
    def reset_password(self, id={"atype":int, "adef":0}):
        """
        后台重置密码
        """
        try:
            r, desc = user_ctrl.reset_password(id=id)
            if not r:
                r_status = "failure"
            else:
                r_status = "success"
        except Exception as e:
            self._logging.error(e)
            r_status = "error"
            desc = e
        ans = self._return_ans(r_status, desc, "update_password")
        return self._write(ans)

    @POST
    def email(self, email={"atype":str, "adef":""}):
        """
        通过邮箱找回密码
        """
        if not email:
            return self._html_render("user/email.html", {}) 
        else:
            flag, obj = user_ctrl.get_user(email=email)
            ans = {}
            if not flag:
                ans = self._return_ans("error", "没有此用户", "find_password")
                self._logging.error("没有此用户")
                return self._write(ans)
            id = obj[0].id
            session = user_ctrl._password_encrypt(str(datetime.datetime.now())+str(id))
            self._set_user_passwd_session(id=id, ses=session)
            # 现在需要发送邮件了
            html = "templates/email/passwd.html"
            txt = "templates/email/passwd.txt"
            to = email
            kwargs = {}
            kwargs["email"] = email
            kwargs["time"] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            kwargs["url"] = "/user/user/find_passwd?id=%s&session=%s" %(str(id), session)
            flag, desc = send_email(html=html, text=txt, To=to, kwargs=kwargs)
            if flag:
                r_status = "success"
            else:
                r_status = "failure"
            ans = self._return_ans(r_status, desc, "send_email")
            return self._write(ans)

    @POST
    def find_passwd(self, id={"atype":int, "atype":""},
            session={"atype":str, "atype":""},
            password={"atype":str, "atype":""},
            q={"atype":str, "atype":""}
        ):
        """
        找回密码
        """
        if not password:
            return self._html_render("user/find_passwd.html", {"id":id, "session":session}) 
        else:
            ans = {}
            if not q:
                ans = self._return_ans("error", "非法找回密码", "find_password")
                self._logging.error("非法找回密码")
                return self._write(ans)
            passwd_session = self._get_user_passwd_session()
            if not user_ctrl.check(passwd_session, id, session):
                ans = self._return_ans("error", "伪装他人找回密码", "find_password")
                self._logging.error("伪装他人找回密码")
                return self._write(ans)
            try:
                r, desc = user_ctrl.reset_password(new_password=password, id=id)
                if not r:
                    r_status = "failure"
                else:
                    r_status = "success"
            except Exception as e:
                self._logging.error(e)
                r_status = "error"
                desc = e
            ans = self._return_ans(r_status, desc, "find_password")
            return self._write(ans)

    @check_login(UPDATE)
    @POST
    def update_status(self, id={"atype":int, "adef":0}, 
            status={"atype":int, "adef":0}
        ):
        """
        更新用户状态
        """
        try:
            r, desc = user_ctrl.update(id=id, kwargs=dict({"status":status}))
            if not r:
                r_status = "failure"
                desc = "更新用户状态失败"
            else:
                r_status = "success"
                desc = "更新用户状态成功"
        except Exception as e:
            self._logging.error(e)
            r_status = "error"
            desc = e
        ans = self._return_ans(r_status, desc, "update_status")
        return self._write(ans)

    @check_login(ROOT)
    @POST
    def update_permission(self, id={"atype":int, "adef":0},
            permission={"atype":int, "adef":0}
        ):
        """
        更新用户权限
        """
        try:
            r, desc = user_ctrl.update(id=id, kwargs=dict({"permission":permission}))
            if not r:
                r_status = "failure"
                desc = "更新用户权限失败"
            else:
                r_status = "success"
                desc = "更新用户权限成功"
        except Exception as e:
            self._logging.error(e)
            r_status = "error"
            desc = e
        ans = self._return_ans(r_status, desc, "update_permission")
        return self._write(ans)


    @check_login(ROOT)
    def list(self, page_num={"atype":int, "adef":1}, 
            page_size={"atype":int, "adef":10},
            contain={"atype":unicode, "adef":""}
        ):
        """
        用户列表
        """
        ans = {}
        try:
            kwargs = {}
            kwargs["contain"] = contain
            total, desc = user_ctrl.list(page_num=int(page_num),
                    page_size=int(page_size), q=contain)
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
                        if not field == "password":
                            value = getattr(d, field)
                            query_dict[field] = value
                    query.append(query_dict)
                kwargs['total_num'] = total
                kwargs['len'] = len(query)
                kwargs['page_num'] = page_num
                kwargs['page_total'] = total / int(page_size) if not total % int(page_size) else total / int(page_size) + 1
            ans = self._return_ans(status, query, "user_list", kwargs)
        except Exception as e:
            self._logging.error(e)
            ans = self._return_ans("error", e, "user_list")
        return self._html_render("user.html", ans)



