# coding:utf8
# author:Coding


import tornado.web
import tornado.ioloop
import settings
import urls
from tornado.web import authenticated
from tornado import gen
import logging
import bcrypt
from tornado.options import define, options
import uuid
import os
from cStringIO import StringIO
import base64
import json
from datetime import date
from datetime import datetime
from PIL import Image
from do import *
import markdown
import requests
import re
from jw import *
from cp_main import *
from tushu import *


class BaseHandler(tornado.web.RequestHandler):  # 基类

    def get_current_user(self):
        username = self.get_secure_cookie("username")
        password = self.get_secure_cookie('password')
        if username and password and check_user_pass(username,
                                                     password):
            return username
        return None


class Index(tornado.web.RequestHandler):  # 文章首页

    def get(self):
        blog = do_get_article()
        self.render('test.html', blog_list=blog, last_id=2)


class get_more(tornado.web.RequestHandler):  # 获取更多文章

    def post(self):
        blog_list = []
        blog = {}
        last = self.get_argument("last")
        limit = self.get_argument("amount")
        limit = int(last) + 5
        res = do_get_more(last, limit)
        for rez in res:
            title = "<a href='page?uid=%s' target='_blank'>" % (
                rez["uuid"]) + rez["title"] + '</a>'
            list_footer = "<a href='page?uid=%s' target='_blank'>" % (
                rez["uuid"]) + u"阅读全文" + '</a>'
            blog = {"title": title, "date_time": rez["date_time"], "content": rez[
                "content"], "list-footer": list_footer}
            blog_list.append(blog)
        self.set_header("Content-Type", "application/json")
        data = json.dumps(blog_list)
        self.write(data)


class Article_info(tornado.web.RequestHandler):  # 文章详情

    def get(self):
        uid = self.get_argument("uid")
        print uid
        blog = do_get_article_info(uid=uid)
        self.render("arcticle_info.html", blog=blog)
# End
# -------------------------------------------------------------------------
'''后台管理'''


class Login(BaseHandler):  # 登陆后台

    def get(self):
        if self.get_argument('next', ''):
            err_mess = '请输入正确的用户名密码'
        else:
            err_mess = ''
        self.render("login.html", error=err_mess)

    def post(self):
        username = self.get_argument('username', '')  # 获取form中username的值
        password = self.get_argument('password', '')  # 获取form中password的值
        self.set_secure_cookie("username", username)
        self.set_secure_cookie("password", password)
        self.redirect("/admin/blog")


class Logout(BaseHandler):  # 退出登陆

    @authenticated
    def get(self):
        self.clear_cookie("username")
        self.clear_cookie("password")
        self.redirect(self.get_argument("next", "/admin/login"))


class Admin(BaseHandler):  # 后台管理界面

    @authenticated
    def get(self):
        self.render("admin.html")


class Article_list(BaseHandler):  # 增加文章 详情列表，状态

    @authenticated
    def get(self):

        blog = do_get_article_list()

        self.render('admin_article_list.html', blog_list=blog)


class Del_Article(BaseHandler):  # 删除文章

    @authenticated
    def get(self):
        uid = self.get_argument("del_uid")
        print uid
        do_del_Article(uid=uid)
        self.redirect("/admin/blog/get_Article")


class editor(BaseHandler):  # 增加文章

    @authenticated
    def get(self):
        tags = do_get_tag()
        self.render("admin_editor0.html", tags=tags)

    def post(self):
        title = self.get_argument("title", '')
        gender = self.get_argument('gender', '')
        publishd = self.get_argument("publishd")
        conter = self.get_argument('editormd-html-code', '')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        write_article(title, gender, conter, int(publishd), now)

        self.redirect('/admin/blog/Editor')


class update_Article(BaseHandler):  # 编辑文章/更新文章

    @authenticated
    def get(self):
        uid = self.get_argument("get_uid")
        blog = do_edit_Article(uid=uid)
        tags = do_get_tag()
        self.render("admin_update_article.html", blog=blog, tags=tags)

    @authenticated
    def post(self):
        uid = self.get_argument("uuid")
        title = self.get_argument("title")
        tag = self.get_argument("gender")
        publishd = self.get_argument("publishd")
        conter = self.get_argument("editormd-html-code")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        do_update_Article(uid, title, conter, tag, int(publishd), now)

        self.redirect("/admin/blog/get_Article")


class Classes(BaseHandler):  # 分类

    @authenticated
    def get(self):
        self.render("admin_classes.html")


class uploadimage(BaseHandler):  # 上传图片

    @authenticated
    def post(self):
        global bb
        upload_path = os.path.join(os.path.dirname(__file__), 'files')
        files = self.request.files['editormd-image-file']
        for meta in files:
            filename = meta['filename']
            filepath = os.path.join(upload_path, filename)
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
            url = str("files/?id=" + filename)
        response = {"success": 1, "message": "上传成功", "url": url}
        response = json.dumps(response)
        self.write(response)


class get_image(BaseHandler):

    def get(self):
        aa = self.get_argument("id", '')
        self.set_header('Content-Type', 'image/jpg')
        with open("files/%s" % aa, 'rb') as rd:
            im = rd.read()
        self.write(im)


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class tag(BaseHandler):

    @authenticated
    def get(self):
        self.render('admin_tags0.html', sort_list=do_get_tag(),
                    count=do_count_tag())


class del_tag(BaseHandler):  # 删除分类

    @authenticated
    def get(self):
        uuid = self.get_argument('del_id')
        if uuid is not None:
            do_del_tag(uuid=uuid)
        self.redirect('/admin/blog/tags')


class add_tag(BaseHandler):  # 添加分类

    @authenticated
    def get(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = self.get_argument('name')
        print name
        if name is not None:
            do_add_tag(name, now)
        self.redirect('/admin/blog/tags')


class update_tag(BaseHandler):  # 更新分类

    @authenticated
    def get(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = self.get_argument("tagname")
        uuid = self.get_argument("uuid")
        if name and uuid is not None:
            do_edit_tag(uuid, name, now)
        self.redirect('/admin/blog/tags')


class setting(BaseHandler):  # 修改账号/密码

    @authenticated
    def get(self):
        self.render('admin_setings0.html')

    def post(self):
        username = self.get_argument('username', '')  # 获取form中username的值
        password = self.get_argument('password', '')  # 获取form中password的值
        if username and password is not None:
            change_user_pass(username, password)
        self.redirect("/admin/login")


class aboutme(BaseHandler):  # 关于我

    @authenticated
    def get(self):
        self.render("admin_aboutme.html")

# End
# -------------------------------------------------------------------------
'''校园业务'''


class cp(tornado.web.RequestHandler):  # 学生晨跑查询

    def get(self):

        name = self.get_argument("username")
        passwd = self.get_argument("password")

        data = {'userName': name,
                'passwd': passwd
                }
        s = requests.Session()
        s.post('http://share.zjtie.edu.cn/student/checkUser.jsp', data=data)
        cprez = s.get('http://share.zjtie.edu.cn/student/queryExerInfo.jsp')
        ress = cprez.text
        re_info = re.compile(r"学号:.*?姓名:(.+?)<".decode("utf8"))
        re_count = re.compile(r"(\d+).*次".decode("utf8"), re.M)

        try:
            name = re_info.findall(ress)[0]
            count = re_count.findall(ress)[0]
            data = {"statuscode": 200, "name": name, "count": count}
            self.set_header(
                "Content-Type", "application/x-www-from-urlencoded")
            self.write(data)
        except:
            self.set_header("Content-Type", "application/json")
            data = {"statuscode": 400}
            self.write(data)


class jwc(tornado.web.RequestHandler):  # 教务成绩查询

    def get(self):
        name = self.get_argument("username")
        passwd = self.get_argument("password")
        do = zfspider(name, passwd)
        try:
            do.ssl_login()
            do.zf_login()
            aa = do.zf_get_cj()
            self.set_header("Content-Type", "application/json")
            cjlist = {"cjlist": aa}
            data = json.dumps({"statuscode": 200, "data": cjlist})
            self.write(data)
        except:
            self.set_header("Content-Type", "application/json")
            data = json.dumps({"statuscode": 400})
            self.write(data)


class tushu_query(tornado.web.RequestHandler):  # 学校图书查询

    def get(self):
        name = self.get_argument("username")
        passwd = self.get_argument("password")
        do = tushus(name, passwd)
        try:
            dd = do.get_info()
            self.set_header("Content-Type", "application/json")
            self.write({"statuscode": 200, "data": dd})
        except:
            self.set_header("Content-Type", "application/json")
            data = json.dumps({"statuscode": 400})
            self.write(data)


class cp_admin(BaseHandler):  # 学生信息

    @authenticated
    def get(self):
        info = do_get_student_info()
        self.render('cp.html', info_list=info)


class add_cp_admin(BaseHandler):  # 添加学生信息

    @authenticated
    def get(self):
        self.render('add_cp.html')

    @authenticated
    def post(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        xh = self.get_argument("xh")
        name = self.get_argument("name")
        mm = self.get_argument("mm")
        email = self.get_argument("email")
        do_add_student_info(xh, name, mm, email, 0, now)
        self.redirect('/admin/blog/add_cp')


class Update_Student_info(BaseHandler):  # 更新学生信息

    @authenticated
    def get(self):
        uid = self.get_argument("get_uid")
        info = do_get_student_info_one(uid)
        self.render("edit_cp.html", info=info)

    @authenticated
    def post(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = self.get_argument('get_uid')
        xh = self.get_argument("xh")
        name = self.get_argument("name")
        mm = self.get_argument("mm")
        email = self.get_argument("email")
        do_Update_Student_info(uid, xh, name, mm, email, now)
        self.redirect('/admin/blog/cp')


class Del_Student_info(BaseHandler):  # 删除学生信息

    @authenticated
    def get(self):
        uid = self.get_argument("del_uid")
        do_Del_Student_info(uid)
        self.redirect('/admin/blog/cp')


def cp_tui():  # 晨跑推送
    info_list = db.Student_info.find()
    for info in info_list:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bb = EmailPush(info['xh'], info['mm'], info['pup_add'])
        try:
            infoo = bb.cp_query()
            if info['count'] == infoo["count"]:
                continue
            else:
                do_Update_Student_info_one(info['xh'], infoo["count"], now)
                bb.send_mail(info['pup_add'], infoo['info'], 'Coding')
        except Exception, e:
            return False


class Application(tornado.web.Application):  # 启动web应用

    def __init__(self):
        us = []
        env = globals()
        for route in urls.urls:
            if len(route) > 1:
                url, handler_name = route
                handler = env.get(handler_name, None)
                us.append((url, handler))

        tornado.web.Application.__init__(self, us, **settings.TORNADO_SETTINGS)

if __name__ == '__main__':
    app = Application()
    app.listen(8888)
    # tornado.ioloop.PeriodicCallback(cp_tui, 3600000).start()
    tornado.ioloop.IOLoop.current().start()
