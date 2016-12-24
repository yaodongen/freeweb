#! /usr/bin/python
# -*- coding:utf8 -*-
import tornado.web
import re
import hashlib
import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__,"../../")))
from settings import db

EMAIL_PAT=re.compile(r"[\w\.]{1,20}@[\w\.]{1,10}")
PHONE_PAT=re.compile(r"\d{11}")
PASSWORD_PAT=re.compile(r"^[^;\"\'\-\\]{0,100}$")



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def _get_user_type(self):
        """ 记录用户的类型 0:普通用户 1:登录用户 2:捐助用户 """
        data=self.get_secure_cookie("user_type")
        return data and int(data)

    def update_err_code(self,dc_data):
        dc_data["err_code"] = dc_data.get("err_code",0) or int(self.get_argument("err_code", 0))

    def _get_account_info(self,data_type,with_prefix=True):
        """ 返回用户该类型的端口密码 """
        type_name = {0:"public_", 1:"login_", 2:"donate_"}
        prefix = with_prefix and type_name[data_type] or ""
        data={}
        if data_type <= 1:
            data = db.get("select port as %sport ,password as %spassword from ssserver where state>0 and type=%s order by used limit 1;"%(prefix,prefix,data_type))
            if data:
                db.execute("update ssserver set used=used+1 where port=%s", data["%sport"%prefix])
        elif data_type==2:
            data = db.get("select port as %sport ,password as %spassword from ssserver where state>0 and type=2 and owner=\"%s\" limit 1"%(prefix,prefix,self.get_current_user()))
            if not data:
                """ 尝试分配 """
                db.execute("update ssserver set owner=%s where owner is null and type=2 limit 1", self.get_current_user())
                data = db.get("select port as %sport ,password as %spassword from ssserver where state>0 and type=2 and owner=\"%s\" "%(prefix,prefix,self.get_current_user()))
        return data

    def get_user_info(self):
        data={
            "public_port":None,
            "public_password":None,
            "login_port":None,
            "login_password":None,
            "donate_port":None,
            "donate_password":None,
            "user":None, 
        }
        data.update(self._get_account_info(0) or {})
        if self.current_user:
            data["user"]=self.current_user
        if self._get_user_type()>=1:
            data.update(self._get_account_info(1) or {})
        if self._get_user_type()>=2:
            data.update(self._get_account_info(2) or {"err_code":2000})
        return data




class MainHandler(BaseHandler):
    def get(self):
        # name = tornado.escape.xhtml_escape(self.current_user)
        data = self.get_user_info()
        self.update_err_code(data)
        self.render("home.html",**data)


class LoginHandler(BaseHandler):
    def get(self):
        self.redirect("/?err_code=1002")

    def post(self):
        user=self.get_argument("user")
        password=self.get_argument("password")
        err_code=0 
        user_type=0
        if EMAIL_PAT.match(user) or PHONE_PAT.match(user):
            password=hashlib.sha256(password).hexdigest()
            # old user
            if db.query("select * from user where user=%s",user):
                result=db.get("select type from user where user=%s and password=%s limit 1", user, password)
                if result:
                    user_type=result["type"]
                else:
                    err_code=1001
            # new user
            else:
                db.execute("insert into user(user,password,create_time,total_flow) values (%s,%s,current_timestamp,0)",user,password) 
                user_type=1
                err_code=False
        else:
            err_code=1000
        if not err_code:
            user=self.set_secure_cookie("user", self.get_argument("user"))
            user_type=self.set_secure_cookie("user_type", str(user_type))
            self.redirect("/")
        else:
            self.redirect("/?err_code=%s"%err_code)


class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        template_data=self.get_user_info()
        self.update_err_code(template_data)
        if self.get_argument("log_out", False):
            self.clear_cookie("user")
            self.clear_cookie("user_type")
            self.redirect("/")
            return 
        data=db.get("select used_flow,total_flow,donate_money,create_time from user where user=%s limit 1",self.current_user)
        template_data.update(data) 
        self.render("user.html",**template_data)


class DonateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        money=self.get_argument("money",0)
        template_data=self.get_user_info()
        self.update_err_code(template_data)
        template_data["money"]=money
        self.render("donate.html",**template_data)

    @tornado.web.authenticated
    def post(self):
        money=int(self.get_argument("money","0"))
        if money > 0:
            db.execute("update user set type=2,donate_money=donate_money+%s,total_flow=2048 where user=%s",money, self.current_user)
            user_type=self.set_secure_cookie("user_type", "2")
        self.redirect("/")
