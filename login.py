import requests
from bs4 import BeautifulSoup
import simplejson
import time
from PIL import Image
from http import cookiejar
import os


######面向对象
class Loginzh:
    def __init__(self, agent, headers, session):
        self.agent = agent
        self.headers = headers
        self.session = session
        self.xsrf_token = ""

    def get_prepertion(self):
        homeurl = 'https://www.zhihu.com'
        homeresponse = self.session.get(url=homeurl, headers=self.headers)
        homesoup = BeautifulSoup(homeresponse.text, 'html.parser')
        xsrfinput = homesoup.find('input', {'name': '_xsrf'})
        self.xsrf_token = xsrfinput['value']
        print("获取到的xsrf_token为： ", self.xsrf_token)

    def get_captcha(self):
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time() * 1000))
        response = self.session.get(captcha_url, headers=self.headers)
        with open('captcha.gif', 'wb') as f:
            f.write(response.content)
            f.close()
        try:
            img = Image.open('captcha.gif')
            img.show()
            img.close()
        except:
            pass
        captcha = {
            'img_size': [200, 44],
            'input_points': [],
        }
        points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20],
                  [129.796875, 22],
                  [150.796875, 22]]
        seq = input('请输入倒立字的位置\n>')
        for i in seq:
            captcha['input_points'].append(points[int(i) - 1])
        return simplejson.dumps(captcha)

    def get_login(self):
        self.headers['X-Xsrftoken'] = self.xsrf_token
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        loginurl = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': self.xsrf_token,
            'phone_num': '......',
            'password': '.......',
            'captcha_type': 'cn',
            'captcha': self.get_captcha()
        }
        loginresponse = self.session.post(url=loginurl, headers=self.headers, data=postdata)
        print('服务器端返回响应码：', loginresponse.status_code)
        r = self.session.get(url="https://www.zhihu.com/people/edit", headers=self.headers)
        print(r.text)


agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}
session = requests.Session()
loginRespond = Loginzh(agent, headers, session)
loginRespond.get_prepertion()
loginRespond.get_login()

######面向过程
# 构造 Request headers
# agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
# headers = {
#     "Host": "www.zhihu.com",
#     "Referer": "https://www.zhihu.com/",
#     'User-Agent': agent
# }
######### 构造用于网络请求的session
# session = requests.Session()

############ 获取_xsrf && X-Xsrftoken
# homeurl = 'https://www.zhihu.com'
# homeresponse = session.get(url=homeurl, headers=headers)
# homesoup = BeautifulSoup(homeresponse.text, 'html.parser')
# xsrfinput = homesoup.find('input', {'name': '_xsrf'})
# xsrf_token = xsrfinput['value']
# print("获取到的xsrf_token为： ", xsrf_token)

# def get_captcha():
#     # 验证码URL是按照时间戳的方式命名的
#     captcha_url = 'https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (int(time.time() * 1000))
#     response = session.get(captcha_url, headers=headers)
#     # 保存验证码到当前目录
#     with open('captcha.gif', 'wb') as f:
#         f.write(response.content)
#         f.close()
#
#     # 自动打开刚获取的验证码
#
#     try:
#         img = Image.open('captcha.gif')
#         img.show()
#         img.close()
#     except:
#         pass
#
#     captcha = {
#         'img_size': [200, 44],
#         'input_points': [],
#     }
#     points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20], [129.796875, 22],
#               [150.796875, 22]]
#     seq = input('请输入倒立字的位置\n>')
#     for i in seq:
#         captcha['input_points'].append(points[int(i) - 1])
#     return simplejson.dumps(captcha)

########### 开始登陆
# headers['X-Xsrftoken'] = xsrf_token
# headers['X-Requested-With'] = 'XMLHttpRequest'
# loginurl = 'https://www.zhihu.com/login/phone_num'
# postdata = {
#     '_xsrf': xsrf_token,
#     'phone_num': '18482175910',
#     'password': 'lyh19951020',
#     'captcha_type': 'cn',
#     'captcha': get_captcha()
#  }
# loginresponse = session.post(url=loginurl, headers=headers, data=postdata)
# print('服务器端返回响应码：', loginresponse.status_code)
#
# r = session.get(url="https://www.zhihu.com/people/edit", headers=headers)
# print(r.text)
# 请求后自动更新cookie
# r = session.get(url)
# if r.cookies.get_dict():
# session.cookies.update(r.cookies)
