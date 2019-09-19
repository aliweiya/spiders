# -*- coding: utf-8 -*-
# Function : 测试，闹着玩儿嘞
# Author : Elvis CT
# Time : 2019年月日

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}
ip = '163.125.114.108:8118'
proxy = {
    'http': 'http://' + ip,
    'https': 'https://' + ip,
        }
response = requests.get('http://bxjg.circ.gov.cn/web/site0/tab5240/module14430/page1.htm', headers=headers, proxies=proxy, timeout=3)
print(response.text)
"""
<span class="def-price" datasku="10561583946|||||0070067633">
<i>¥</i>39<i>.20</i></span>
"""
