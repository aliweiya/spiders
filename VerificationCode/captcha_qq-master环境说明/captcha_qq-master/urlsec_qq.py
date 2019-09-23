#!/usr/bin/env python
# encoding: utf-8

# -*- coding: utf-8 -*-
# @software: PyCharm
# @time: 2019/9/21 14:48
# @file: urlsec_qq.py
# @desc: 腾讯防水墙滑动验证码破解 https://open.captcha.qq.com/online.html

import numpy as np
import random
from selenium.webdriver import ActionChains
import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from PIL import Image
import os
from selenium.webdriver.support.ui import WebDriverWait
import cv2


class Login(object):
    """
    腾讯防水墙滑动验证码破解
    使用OpenCV库
    成功率大概90%左右：在实际应用中，登录后可判断当前页面是否有登录成功才会出现的信息：比如用户名等。循环
    https://open.captcha.qq.com/online.html
    破解 腾讯滑动验证码
    腾讯防水墙
    python + seleniuum + cv2
    """
    def __init__(self):
        # 如果是实际应用中，可在此处账号和密码
        # 此处初始化一些内容，主要是对模拟浏览器的一个深层次参数配置
        self.url = "https://urlsec.qq.com/report.html"
        self.option = ChromeOptions()
        self.option.add_argument('--user-agent=Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
        self.option.add_argument(r'--user-data-dir=C:\Users\admin\AppData\Local\Google\Chrome\User Data')
        # self.option.add_argument('--disable-extensions')
        # self.option.add_argument('--profile-directory=Default')
        # self.option.add_argument("--incognito")
        # self.option.add_argument("--disable-plugins-discovery")
        # self.option.add_argument("--start-maximized")
        # self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = Chrome(options=self.option)

    # 此处仅为调试用
    @staticmethod
    def show(name):
        cv2.imshow('Show', name)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 此处仅为调试用
    @staticmethod
    def webdriverwait_send_keys(dri, element, value):
        """
        显示等待输入
        :param dri: driver
        :param element:
        :param value:
        :return:
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).send_keys(value)

    @staticmethod
    def webdriverwait_click(dri, element):
        """
        显示等待 click
        :param dri: driver
        :param element:
        :return:
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).click()

    def is_element_exist(self, value):
        # 判断所选择的html元素是否存在，建立一个标志位做后续判断
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(value)
            return flag

        except:
            flag = False
            return flag

    @staticmethod
    def get_postion(chunk, canves):
        """
        判断缺口位置，用opencv判断
        :param chunk: 缺口图片是原图
        :param canves:
        :return: 位置 x, y
        """
        otemp = chunk
        oblk = canves
        target = cv2.imread(otemp, 0)
        template = cv2.imread(oblk, 0)
        # w, h = target.shape[::-1]
        temp = 'temp.jpg'
        targ = 'targ.jpg'
        cv2.imwrite(temp, template)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        template = cv2.imread(temp)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)
        return x, y
        # # 展示圈出来的区域
        # cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
        # cv2.imwrite("yuantu.jpg", template)
        # show(template)

    # @staticmethod
    # def get_track(distance):
    #     """
    #     模拟轨迹 假装是人在操作
    #     :param distance:
    #     :return:
    #     """
    #     # 初速度
    #     v = 0
    #     # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    #     t = 0.2
    #     # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    #     tracks = []
    #     # 当前的位移
    #     current = 0
    #     # 到达mid值开始减速
    #     mid = distance * 7 / 8
    #
    #     distance += 18  # 先滑过一点，最后再反着滑动回来
    #     # a = random.randint(1,3)
    #     while current < distance:
    #         if current < mid:
    #             # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
    #             a = random.randint(2, 4)  # 加速运动
    #         else:
    #             a = -random.randint(3, 5)  # 减速运动
    #
    #         # 初速度
    #         v0 = v
    #         # 0.2秒时间内的位移
    #         s = v0 * t + 0.5 * a * (t ** 2)
    #         # 当前的位置
    #         current += s
    #         # 添加到轨迹列表
    #         tracks.append(round(s))
    #
    #         # 速度已经达到v,该速度作为下次的初速度
    #         v = v0 + a * t
    #
    #     # 反着滑动到大概准确位置
    #     for i in range(6):
    #         tracks.append(-random.randint(2, 3))
    #     for i in range(6):
    #         tracks.append(-random.randint(1, 3))
    #     return tracks

    @staticmethod
    def get_track(distance):
        """ 模拟轨迹 假装是人在操作 """

        """ 1.设定长度比例 """
        pos = [0, 1, 2, 3, 3, 2, 1, 2, 2, 1]  # 滑动轨迹之间比例设定

        """ 2. 正弦函数 """
        # pos = [random.randrange(0, 10) for i in range(10)]
        # pos.sort()
        # pos = [item / 10 * math.pi for item in pos]
        # pos = [math.sin(x) for x in pos]

        pos_sum = sum(pos)
        route = [int(int(distance) * (item / pos_sum)) for item in pos]  # 计算出移动路径

        route = route + [int(distance)-sum(route), ]

        print('distance', distance)
        print('sum route', sum(route))
        print('route', route)
        return route

    @staticmethod
    def urllib_download(imgurl, imgsavepath):
        """
        下载图片
        :param imgurl: 图片url
        :param imgsavepath: 存放地址
        :return:
        """
        from urllib.request import urlretrieve
        urlretrieve(imgurl, imgsavepath)

    def after_quit(self):
        """
        关闭浏览器
        :return:
        """
        self.driver.quit()

    def login_main(self, driver):
        # 从Windows切换到滑块Frame
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_id('tcaptcha_iframe'))  # switch 到 滑块frame

        # 获取滑块大图
        bk_block = driver.find_element_by_xpath('//img[@id="slideBg"]')  # 大图
        web_image_width = bk_block.size
        web_image_width = web_image_width['width']  # 网页图片宽度
        bk_block_x = bk_block.location['x']  # 网页图片位置x

        # 获取滑块碎片
        slide_block = driver.find_element_by_xpath('//img[@id="slideBlock"]')  # 小滑块
        slide_block_x = slide_block.location['x']  # 网页滑块位置x

        # 获取大图小图以及操作按钮
        bk_block = driver.find_element_by_xpath('//img[@id="slideBg"]').get_attribute('src')       # 大图 url
        slide_block = driver.find_element_by_xpath('//img[@id="slideBlock"]').get_attribute('src')  # 小滑块 图片url
        slid_ing = driver.find_element_by_xpath('//div[@id="tcaptcha_drag_thumb"]')  # 滑块

        # 图片保存
        os.makedirs('./image/', exist_ok=True)
        self.urllib_download(bk_block, './image/bkBlock.png')
        self.urllib_download(slide_block, './image/slideBlock.png')
        time.sleep(0.5)

        # 打开图片获取尺寸信息，判断缺口位置，模拟轨迹
        img_bkblock = Image.open('./image/bkBlock.png')
        real_width = img_bkblock.size[0]
        width_scale = float(real_width) / float(web_image_width)  # 计算网页图片与实际图片的比例
        position = self.get_postion('./image/bkBlock.png', './image/slideBlock.png')  # 获取实际图片distance的绝对值
        real_position = position[1] / width_scale  # 获取网页像素的相对值
        real_position = real_position - (slide_block_x - bk_block_x)  # 获取要移动的距离
        track_list = self.get_track(real_position + 4)

        # 拖动滑动条按钮，验证码识别
        ActionChains(driver).click_and_hold(on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
        time.sleep(0.2)

        # print('第二步,拖动元素')
        for track in track_list:
            ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
            time.sleep(random.randint(1, 10) * 0.001)
        ActionChains(driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform()   # 微调，根据实际情况微调
        ActionChains(self.driver).move_by_offset(xoffset=-2, yoffset=0).perform()  # 模仿正常松鼠标操作
        ActionChains(self.driver).move_by_offset(xoffset=2, yoffset=0).perform()
        # print('第三步,释放鼠标')
        ActionChains(driver).release(on_element=slid_ing).perform()

    def main(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.url)
        vcode = driver.find_element_by_id('vcode')
        self.webdriverwait_click(driver, vcode)
        time.sleep(1)

        time.sleep(0.5)
        for i in range(20):
            self.login_main(driver)
            time.sleep(3)
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="loading_animation"]/iframe'))  # switch 到 滑块frame
            flag = self.is_element_exist("//div/div/p[text()='验证成功']")
            print(flag)

            if flag:
                print('Login is Success')
                self.after_quit()
                break
            else:
                print('Login is Failed, Again')


if __name__ == '__main__':
    login = Login()
    login.main()
