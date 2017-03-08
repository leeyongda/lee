# -*- coding:utf-8 -*-
# author:Coding


# cryptor = crypto.SimpleCrypto(settings.COOKIE_SECRET)
# site_info = lambda: kv.get(settings.K_SITE_INFO)
# _site_info = site_info()
# admin_url = _site_info['admin']['url']

urls = [
    (r"/", 'Index'),
    # (r"/index", 'Index'),
    (r"/jwc", 'jwc'),
    (r"/dotushu", 'tushu_query'),
    (r"/test", 'jtest'),
    (r"/p/(.*?)", 'article_info'),
    (r"/", 'page'),
    (r"/?page=(.*?)", "get_page"),
    (r"/search", "search"),

    (r"/admin/login", 'Login'),
    (r'/admin/logout', 'Logout'),
    (r"/admin/blog", "Admin"),

    (r"/admin/blog/get_Article", "Article_list"),
    (r"/admin/blog/get_Article/(.*?)", "Article_list"),
    (r"/admin/blog/Add_Article", 'AddArticle'),
    (r"/admin/blog/Edit_Article", 'EditArticle'),
    (r"/admin/blog/update_Article", 'update_Article'),
    (r"/admin/blog/aboutme", 'aboutme'),

    (r"/admin/blog/Del_Article", 'Del_Article'),
    (r"/admin/blog/uploadimage", 'uploadimage'),
    (r"/admin/blog/Editor", "editor"),
    (r"/admin/blog/Classes", "Classes"),
    (r"/admin/blog/settings", "setting"),

    (r"/admin/blog/tags", 'tag'),
    (r"/admin/blog/del_tag", "del_tag"),
    (r"/admin/blog/add_tag", "add_tag"),

    (r"/del_tag", "del_tag"),
    (r"/add_tag", "add_tag"),
    (r"/update_tag", "update_tag"),
    # (r"/admin/blog/files/", 'getmage')

    (r"/admin/blog/files/(?:.*?)", "get_image"),
    (r"/cptest", 'cp'),
    (r"/admin/blog/cp", 'cp_admin'),
    (r"/admin/blog/add_cp", 'add_cp_admin'),
    (r"/admin/blog/Update_Student_info", 'Update_Student_info'),
    (r"/admin/blog/Del_Student_info", 'Del_Student_info'),

]
