#!/usr/bin/env python
# encoding: utf-8

# -*- coding: utf-8 -*-
# @software: PyCharm
# @time: 2019/9/21 14:48
# @file: baidu_demo.py
# @desc: selenium功能测试，对简书的访问

# C:\Users\adm|in\AppData\Local\Google\Chrome\User Data\Default
from time import sleep

from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver import ChromeOptions

profile_directory = r'--user-data-dir=C:\Users\admin\AppData\Local\Google\Chrome\User Data'
option = webdriver.ChromeOptions()
option.add_argument(profile_directory)
driver = webdriver.Chrome(chrome_options=option)
driver.get('https://www.jianshu.com/')
sleep(3)
driver.close()
