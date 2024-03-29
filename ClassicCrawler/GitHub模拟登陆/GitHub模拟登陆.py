# -*- encoding: utf-8 -*-
# @Author   : 漫天丶飞雪
# @Created  : 2019-10-14 16:14
# @IDE      : PyCharm
# @Version  : Python 3.6.0
# @Function : 模拟登陆GitHub

'''
模拟Github登陆步骤：
    1、请求头:self.headers,请求url
    2、设置session,保存登陆信息cookies,生成github_cookie文件
    3、POST表单提交,请求数据格式post_data
    4、authenticity_token获取
    5、在个人中心验证判断是否登陆成功,输出个人中心信息即登陆成功

'''

import requests
from lxml.html import etree
import urllib3
import http.cookiejar as cookielib

urllib3.disable_warnings()


class GithubLogin():
    def __init__(self):
        # url
        self.loginUrl = 'https://github.com/login'
        self.postUrl = 'https://github.com/session'
        self.profileUrl = 'https://github.com/settings/profile'

        # 设置请求头
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }

        # 设置session
        self.session = requests.session()
        # 生成github_cookie文件
        self.session.cookies = cookielib.LWPCookieJar(filename='github_cookie')

    '''
        登陆时表单提交参数
        Form Data:
            commit:Sign in
            utf8:✓
            authenticity_token:yyZprIm4aghZ0u7r25ymZjisfTjGdUAdDowD9fKHM0oUvHD1WjUHbn2sW0Cz1VglZWdGno543jod2M8+jwLv6w==
            login:*****
            password:******

    '''

    def post_account(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.get_token(),
            'login': email,
            'password': password
        }
        response = self.session.post(self.postUrl, data=post_data, headers=self.headers)
        # 保存cookies
        self.session.cookies.save()

    def load_cookie(self):
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print('cookie 获取不成功')

    # 获取authenticity_token
    def get_token(self):
        response = self.session.get(self.loginUrl, headers=self.headers, verify=False)
        html = etree.HTML(response.text)
        authenticity_token = html.xpath('//div[@id="login"]//input[@name="authenticity_token"]/@value')[0]
        return authenticity_token

    # 判断是否登陆成功
    def isLogin(self):
        self.load_cookie()
        response = self.session.get(self.profileUrl, headers=self.headers)
        selector = etree.HTML(response.text)
        name = selector.xpath('//dl[@class="form-group"]//input/@value')
        # 登陆成功返回来的个人设置信息
        print(u'个人设置Profile标题: %s' % name)


if __name__ == "__main__":
    github = GithubLogin()
    # 输入自己email账号和密码
    github.post_account(email='******', password='******')
    # 验证是否登陆成功
    github.isLogin()
