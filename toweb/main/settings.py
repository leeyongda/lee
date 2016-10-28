#coding:utf8
import os
import os.path as osp
import inspect
import pymongo


TORNADO_SETTINGS = {
"debug":True,
"login_url":"/admin/login",
# "xsrf_cookies": True,
"cookie_secret":"bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
'template_path':osp.join(osp.dirname(__file__), "templates"),
"static_path": os.path.join(os.path.dirname(__file__), "static"),
"upload_path":os.path.join(os.path.dirname(__file__),'files'),
"image_path":os.path.join(os.path.dirname(__file__),'dist'),
'db' : pymongo.Connection('localhost', 27017)
}
