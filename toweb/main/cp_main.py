# -*- coding:utf-8 -*-
# author:Coding
# python_version:2.7.11
# date:2016-05-23 16:53:30

import re
import smtplib
import requests
from email.mime.text import MIMEText


class EmailPush(object):

    def __init__(self, name, password, mail_add):

        self.name = name
        self.password = password
        self.mail_add = mail_add

    def send_mail(self, address, sub, content):  #

        mail_host = "smtp.qq.com"  # 设置服务器

        mail_user = "963189900@qq.com"  # 用户名

        mail_pass = "kjfleqmbdmlpbbjc"  # 口令

        mail_postfix = "qq.com"  # 发件箱的后缀

        me = "【noreply】" + "<" + mail_user + ">"

        # me="【noreply】"+"<"+mail_user+"@"+mail_postfix+">"

        msg = MIMEText(content, _subtype='html', _charset='utf8')

        msg['Subject'] = sub  # 设置主题

        msg['From'] = me

        msg['To'] = address

        try:

            s = smtplib.SMTP()

            s.connect(mail_host)  # 连接smtp服务器

            s.starttls()

            s.login(mail_user, mail_pass)  # 登陆服务器

            s.sendmail(me, address, msg.as_string())  # 发送邮件

            s.close()

            return True

        except Exception, e:

            print str(e)

            return False

    def cp_query(self):

        data = {'userName': self.name,
                'passwd': self.password
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
            info = u'姓名:%s' % name, u'晨跑次数:%s' % count
            info = str(info).decode('unicode-escape').replace("'", "")
            info = info.replace("u", '')
            infp = {"count": count, "info": info}
            return infp
            # if count == '2':
            #     pass
            # else:
            #     aa = EmailPush()
            #     aa.send_mail(self.mail_add, info, 'python')
        except:
            return u'学号/密码错误！'
