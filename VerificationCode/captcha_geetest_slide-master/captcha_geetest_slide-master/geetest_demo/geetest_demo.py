#!/usr/bin/env python
# encoding: utf-8

# -*- coding: utf-8 -*-
# @software: PyCharm
# @time: 2019/9/21 15:04
# @file: geetest_demo.py
# @desc: 破解极验滑动验证码 https://www.geetest.com/demo/slide-popup.html

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
import time
import random
import math
BORDER = 6


class CrackGeetest(object):
    def __init__(self):
        self.url = 'https://www.geetest.com/demo/slide-popup.html'
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10)

    def open(self):
        """
        打开网页
        :return None
        """
        self.browser.get(self.url)

    def close(self):
        """
        关闭网页
        :return None
        """
        self.browser.close()
        self.browser.quit()

    def change_to_slide(self):
        """
        切换为滑动认证
        :return 滑动选项对象
        """
        huadong = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.products-content > ul > li:nth-child(2)'))
        )
        return huadong

    def get_geetest_button(self):
        """
        获取初始认证按钮
        :return 按钮对象
        """
        button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.geetest_radar_tip_content'))
        )
        return button

    def wait_pic(self):
        """
        等待验证图片加载完成
        :return None
        """
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_popup_wrap'))
        )

    def get_screenshot(self):
        """
        获取网页整个截图
        :return: 网页整个截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()  # 获取整个页面截图
        self.browser.save_screenshot("yanzhengma1.png")  # 保存上面的这个截图
        screenshot = Image.open(BytesIO(screenshot))  # 打开这个截图并返回
        return screenshot

    def get_position(self):
        """
        获取验证码位置
        :return: 位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_canvas_img.geetest_absolute')))
        time.sleep(0.5)
        location = img.location
        size = img.size
        # top, bottom = location['y'] - size['height'], location['y']
        # print("top")
        # left, right = location['x'], location['x'] + size['width']
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        return top, bottom, left, right

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取极验验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()  # 网页验证码位置 上 下 左 右
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()  # 获取整张网页截图对象
        captcha = screenshot.crop((left, top, right, bottom))  # crop为Image的属性，crop属性可以返回图片中的矩形区域
        captcha.save(name)  # 保存这个矩形区域
        return captcha  # 返回这个网页截图内部的矩形区域

    def delete_style(self):
        """
        执行js脚本，获取无滑块图
        :return None
        """
        js = 'document.querySelectorAll("canvas")[2].style=""'
        self.browser.execute_script(js)

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img1: 不带缺口图片
        :param img2: 带缺口图
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        # print(pix1+"      "+pix2)
        threshold = 60
        if abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(
                pix1[2] - pix2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, img1, img2, pos='start'):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图
        :return 缺口位置
        """
        if pos == 'start':
            left = 0  # 这个是参考值，意思就是从左往右这个位置像素至开始，然后检测缺口所在位置的像素
        else:
            left = 70
        """ 参考 : size=260x160 """
        for i in range(left, img1.size[0]):  # 带缺口图片宽度
            for j in range(img1.size[1]):  # 不带缺口图片宽度
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    # def get_track(self, distance):
    #     """
    #     根据偏移量获取移动轨迹
    #     :param distance: 偏移量
    #     :return: 移动轨迹
    #     """
    #     # 移动轨迹
    #     track = []
    #     # 当前位移
    #     current = 0
    #     # 减速阈值
    #     mid = distance * 3 / 5
    #     # 计算间隔
    #     t = 0.2
    #     # 初速度
    #     v = 0
    #     # 滑超过过一段距离
    #     distance += 15
    #     while current < distance:
    #         if current < mid:
    #             # 加速度为正
    #             a = 2
    #         else:
    #             # 加速度为负
    #             a = -0.5
    #         # 初速度 v0
    #         v0 = v
    #         # 当前速度 v
    #         v = v0 + a * t
    #         # 移动距离 move-->x
    #         move = v0 * t + 1 / 2 * a * t * t
    #         # 当前位移
    #         current += move
    #         # 加入轨迹
    #         track.append(round(move))
    #     return track

    def get_track(self, distance):
        """ 模拟轨迹 假装是人在操作 """

        """ 1.设定长度比例 """
        # pos = [0, 1, 2, 3, 3, 2, 1, 2, 2, 1]  # 滑动轨迹之间比例设定

        """ 2. 正弦函数 """
        pos = [random.randrange(0, 10) for i in range(10)]
        pos.sort()
        pos = [item / 10 * math.pi for item in pos]
        pos = [math.sin(x) for x in pos]

        pos_sum = sum(pos)  # 计算理论滑动像素长度，后面用来补全滑动像素距离
        route = [int(int(distance) * (item / pos_sum)) for item in pos]  # 计算出移动路径

        route = route + [int(distance)-sum(route), 0]

        print('distance', distance)
        print('sum route', sum(route))
        print('route', route)
        return route

    def shake_mouse(self):
        """
        模拟人手释放鼠标时的抖动
        :return: None
        """
        ActionChains(self.browser).move_by_offset(xoffset=-2, yoffset=0).perform()
        ActionChains(self.browser).move_by_offset(xoffset=2, yoffset=0).perform()

    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param tracks: 轨迹
        :return
        """
        back_tracks = [-1, -1, -2, -2, -3, -2, -2, -1, -1]
        ActionChains(self.browser).click_and_hold(slider).perform()
        # 正向
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.002)
        time.sleep(0.5)
        # # 逆向
        # for x in back_tracks:
        #     ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        # 模拟抖动
        self.shake_mouse()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack(self):
        try:
            # 打开网页
            self.open()
            # # 转换验证方式，点击认证按钮
            # s_button = self.change_to_slide()
            # time.sleep(1)
            # s_button.click()
            g_button = self.get_geetest_button()
            g_button.click()
            # 确认图片加载完成，等待模拟器把需要的内容加载出来
            self.wait_pic()
            # 获取滑块对象
            slider = self.get_slider()
            # 获取带缺口的验证码图片
            image1 = self.get_geetest_image('captcha1.png')  # 有滑块截图
            self.delete_style()  # 执行js脚本获取无滑块截图
            image2 = self.get_geetest_image('captcha2.png')  # 无滑块截图
            gap = self.get_gap(image1, image2, pos='end')  # 获取缺口位置
            print('缺口位置', gap)
            BORDER = self.get_gap(image1, image2, pos='start')
            print('滑块位置', BORDER)
            gap -= BORDER  # BORDER为滑块初始位置，视情况而定，
            print('gap', gap)
            track = self.get_track(gap)
            print(track)
            self.move_to_gap(slider, track)  # 移动滑块至缺口位置
            success = self.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功')
            )
            print(success)
            time.sleep(1)  # 如果失败1s后重试
            self.close()
        except:
            print('Failed-Retry')
            self.crack()


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()
