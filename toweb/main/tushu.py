# coding:utf8

import requests

import re
from bs4 import BeautifulSoup


class tushus(object):
    """docstring for tushu"""
    '''图书借阅 ---Python'''

    def __init__(self, name, password):
        self.s = requests.session()
        self.index_url = 'http://m.5read.com/903'
        self.get_url = 'http://mc.m.5read.com/cmpt/opac/opacLink.jspx?stype=1'
        self.post_url = 'http://mc.m.5read.com/irdUser/login/opac/opacLogin.jspx'
        self.name = name
        self.password = password

        self.data = {
            'schoolid': '903',
            'backurl': '',
            'userType': '0',
            'username': self.name,
            'password': self.password
        }
        self.head = {
            'Host': 'mc.m.5read.com',
            'Origin': 'http://mc.m.5read.com',
            'Referer': 'http://mc.m.5read.com/user/login/showLogin.jspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }

    def get_info(self):
        self.s.get(self.index_url)
        self.s.post(
            self.post_url, headers=self.head, data=self.data)
        rez = self.s.get(self.get_url)
        count = re.findall(ur".*我的借阅：(.*?)</td>", rez.text)
        soup = BeautifulSoup(rez.text, "html.parser")
        score_table = soup.find('div', class_='boxBd')
        score_list = []
        cells = score_table.find_all('div', class_='sheet')
        for cell in cells:
            ce = cell.find_all('td')
            xl = ce[0].text.strip()
            sm = ce[1].text.strip()
            rq = ce[2].text.strip()
            xj = ce[3].text.strip()
            score_dict = {"xl": xl, 'sm': sm, 'rq': rq, 'xj': xj}
            score_list.append(score_dict)

        infolist = {"tulist": score_list, "count": count}

        return infolist
# aa = raw_input()
# if __name__ == '__main__':
#     t = tushu('20142168','123456')
#     t.get_info()
