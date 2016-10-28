# coding:utf-8
# author:Coding
# version:python 2.7

import re
import requests
from bs4 import BeautifulSoup
import csv
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
reload(sys)
sys.setdefaultencoding('utf8')

'''
基于Python 爬虫--适用于(浙经院)正方教务处
需要安装2个第三方库
请下载安装即可
pip install requests
pip install BeautifulSoup4
'''


class zfspider(object):

    def __init__(self, name, password):
        self.s = requests.session()
        self.name = name
        self.password = password

    def ssl_login(self):  # 尝试登陆SSL_VPN

        ssl_url = 'https://120.199.18.174/por/login_psw.csp?#http%3A%2F%2Fe.zjtie.edu.cn%2F'
        data = {
            'mitm_result': '',
            'svpn_name': self.name,
            'svpn_password': self.password,
            'svpn_rand_code': '',
        }
        self.s.post(ssl_url, data=data, verify=False)

        return self.s

    def zf_login(self):  # 尝试登陆教务处
        global login_page
        lt = self.s.get(
            'https://120.199.18.174/web/1/https/1/ca.zjtie.edu.cn/zfca/login', verify=False).text
        lt = re.findall(r'<input type="hidden" name="lt" value="(.*?)" />', lt)

        head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': '120.199.18.174',
            'Referer': 'https://120.199.18.174/web/1/https/0/ca.zjtie.edu.cn/zfca/login',
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
        }
        pin_url = "https://120.199.18.174/web/1/https/1/ca.zjtie.edu.cn/zfca/login"  # 验证码地址

        data = {
            'useValidateCode': '0',
            'isremenberme': '0',
            'ip': '',
            'username': self.name,
            'password': self.password,
            'losetime': '30',
            'lt': lt[0],
            '_eventId': 'submit',
            'submit1': ''
        }

        login_page = self.s.post(pin_url, headers=head,
                                 verify=False, data=data).text
        return login_page

    def zf_get_cj(self):  # 获取成绩单

        get_url = re.findall(
            r'<li><a id=".*" onclick=".*" djsl=".*" href="(.*?)" target="_blank">', login_page)

        get_url = get_url[1]
        get_url = get_url.replace("xs_main.aspx", "xscj_gc.aspx")
        url = 'https://120.199.18.174' + get_url
        head = {
            'Referer': 'https://120.199.18.174/web/1/http/0/e.zjtie.edu.cn/portal.do'
        }
        res = self.s.get(url,
                         headers=head, verify=False)

        view = r'name="__VIEWSTATE" value="(.+)" '
        view = re.compile(view)
        rview = view.findall(res.text)[0]  # 获取需要提交的表单值

        data = {
            '__VIEWSTATE': rview,
            'ddlXN': '',
            'ddlXQ': '',
            'Button2': '',
        }
        Referer_url = 'https://120.199.18.174/web/1/http/1/dean.zjtie.edu.cn/xscj_gc.aspx?xh=' + \
            self.name + '&type=1'
        head = {'Referer': Referer_url}
        url = 'https://120.199.18.174/web/1/http/2/dean.zjtie.edu.cn/xscj_gc.aspx?xh=' + \
            self.name + '&type=1'
        cj = self.s.post(url, headers=head, data=data)
        xncj = cj.content
        score_list = []
        soup = BeautifulSoup(xncj, "html.parser")
        score_table = soup.find('table', id='Datagrid1').find_all('tr')

        score_list = []
        score_dict = {}
        info = []
        for score_row in score_table:
            if 'class' in score_row.attrs:
                if score_row.attrs['class'] == ['datelisthead']:
                    continue
            cells = score_row.find_all('td')

            xn = cells[0].text
            xq = cells[1].text
            # kcdm = cells[2].text.strip()
            kcmc = cells[3].text.strip()
            kcxz = cells[4].text.strip()
            xf = cells[6].text
            cj = cells[8].text.strip()
            bkcj = cells[10].text.strip()
            cxcj = cells[11].text.strip()
            score_dict = {"xn": xn, "xq": xq, "kcmc": kcmc, "cj": cj}

            score_list.append(score_dict)

        return score_list
