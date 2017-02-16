# coding:utf-8
import pymongo
import settings
import uuid
import base64

db = settings.TORNADO_SETTINGS['db']
db = db['blogd']


'''晨跑推送'''


def do_get_student_info():
    return db.Student_info.find()


def do_add_student_info(xh, name, mm, email, count, now):
    return db.Student_info.insert(dict(uuid=get_uuid(), xh=xh, name=name,
                                       mm=mm, pup_add=email, count=count, date_time=now))


def do_update_student_info(uid, xh, name, mm, email, now):
    return db.Student_info.update({"uuid": uid}, {"$set": {"xh": xh, "name": name,
                                                           "mm": mm, "pup_add": email, "date_time": now}})


def do_update_student_info_one(xh, count, now):
    return db.Student_info.update({"xh": xh}, {"$set": {"count": count, "date_time": now}})


def do_get_student_info_one(uid):
    return db.Student_info.find_one({'uuid': uid})


def do_del_student_info(uid):
    return db.Student_info.remove({'uuid': uid})

# def do_send_info():
#     return db.Student_info.find()

'''end'''


def do_get_article():
    return db.Article.find().sort([("date_time", -1)])[:2]


def do_get_more(last, limit):

    return db.Article.find().sort([("date_time", -1)])[int(last):int(limit)]


def do_get_article_list():
    return db.Article.find()


def do_get_article_info(uid):
    return db.Article.find_one({'uuid': uid})

'''title标题,tag分类,content内容,puplishd状态(0,1)'''


def write_article(title, abstract ,tag, content, puplishd, now,):
    db.Article.insert(dict(uuid=get_uuid(), title=title, abstract=abstract, tag=tag,
                           content=content, puplishd=puplishd, date_time=now))


def do_del_Article(uid):
    return db.Article.remove({'uuid': uid})


def do_edit_Article(uid):
    return db.Article.find_one({"uuid": uid})


def do_update_Article(uuid, title, content, tag, puplishd, date_time):
    db.Article.update({"uuid": uuid}, {"$set": {"title": title, "content": content,
                                                "tag": tag, "puplishd": puplishd, "date_time": date_time}})


def get_uuid():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes).replace('+', 'B')


def check_user_pass(user):
    # if db.user.find_one({"username": user}):
        # return True
    # return False
    return db.user.find_one({"username": user})


def change_user_pass(user, pwd):
    db.user.update({'uid': 0},
                   {"$set": {'username': user, 'password': pwd}})


def do_get_tag():
    return db.tags.find()


def do_count_tag():
    return db.tags.find().count()


def do_add_tag(name, date_time):
    db.tags.insert(dict(uuid=get_uuid(), name=name, date_time=date_time))
    return True


def do_edit_tag(uuid, value, now):
    db.tags.update({'uuid': uuid},
                   {"$set": {"name": value, "date_time": now}}, False, True)
    return '更新成功'


def do_del_tag(uuid):
    return db.tags.remove({'uuid': uuid})


def do_search(title):
    return db.Article.find({"$or":[{"title":{"$regex":title, "$options":'i'}},{"content":{"$regex":title, "$options":'i'}}]})


