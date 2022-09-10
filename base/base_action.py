# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:base_action.py
@CreateTime:2022/6/26 16:38
"""
import inspect
import logging
import os
import time
from typing import Union, Any

import uiautomator2 as u2
import re
import cv2

from base.error import ElementNotFoundError
from base.my_logger import MyLogging

from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector
from base.config import FIND_ELEMENT_RETRY
from base.config import read_yaml
from my_logger import logger
# logger = MyLogging(name='测试', level=logging.INFO,
#                    file=f"../current_log/{time.time()}.txt", hint_show=True)

test_package = read_yaml().get('package')


class BaseAction(object):
    """基础组件"""
    annotation: Union[str, Any]
    _element: Union[XPathSelector, UiObject]

    def __init__(self, *args, **kwargs):
        """连接设备"""
        self.driver = u2.connect_usb()  # 创建手机对象
        # logger.info('启动APP')
        # self.app_start()  # 启动APP
        self._kwargs = kwargs
        self.resourceId = kwargs.get("resourceId", '')
        self.text = kwargs.get("text", '')
        self.textContains = kwargs.get('textContains', '')
        self.className = kwargs.get("className", '')
        self.xpath = kwargs.get("xpath", '')
        self.description = kwargs.get("description", '')

        self.index = self._kwargs.pop('index', 0)
        self.desc = self._kwargs.pop('desc', '')

    def find_element(self, retries=FIND_ELEMENT_RETRY, timeout=20):
        """返回当前元素
        @param retries: 重试次数
        @param timeout: 超时时间
        """
        logger.info(f'{self.driver.shell("adb devices")} Find element '
                    f'【{self.desc}】{str(self._kwargs)}')
        self._element = self.driver.xpath(self.xpath) if self.xpath else \
            self.driver(**self._kwargs)[self.index]
        while not self._element.wait(timeout=timeout):
            if retries > 0:
                retries -= 1
                logger.warning(f'{os.system("adb devices")} Retry found the '
                               f'element【{self.desc}】{str(self._kwargs)},'
                               f'index:{self.index}')
                time.sleep(2)
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)  # 返回调用者信息
                logger.warning(f'【{caller.function}:{caller.lineno}】Not found '
                               f'element【{self.desc}】{self._kwargs},index:'
                               f'{self.index}')
                return None
        return self._element

    def find_element_by_child(self, ele, retries=FIND_ELEMENT_RETRY,
                              timeout=10, **kwargs):
        """子定位"""
        self.annotation = kwargs.pop("annotation", "")
        logger.info(f'{os.system("adb devices")} find element by'
                    f'child {self.annotation}{str(kwargs)}')
        self._element = ele.find_element().child(kwargs)
        while not self._element.wait(timeout):
            if retries > 0:
                retries -= 1
                logger.warning(f'{self.driver.shell("adb devices")} retry '
                               f'found element by child {self.annotation}'
                               f'{kwargs}')
                time.sleep(1)
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(f'{caller.function}:{caller.lineno} not found'
                               f'element by child{self.annotation}{kwargs}')
                return None
        return self._element

    def child_click(self, ele, retires=FIND_ELEMENT_RETRY, shoot=True,
                    **kwargs):
        """子元素点击
        @param shoot: 截图标记
        @param retires: 重试次数
        @type ele: 父元素
        """
        element = self.find_element_by_child(ele, retires, kwargs)
        if not element:
            raise ElementNotFoundError(f"Not found element{self.annotation}"
                                       f"{kwargs}")

        element.click()
        logger.info(f'Successful click {self.annotation}{kwargs}')

    def click(self, retries=FIND_ELEMENT_RETRY, shoot=True):
        """点击,只封装了常用的几种方式
        @param retries: 重试次数
        @param shoot: 截图标记
        """
        element = self.find_element(retries)
        if not element:
            raise ElementNotFoundError(f"Not found element【{self.desc}】:"
                                       f"{self._kwargs},index:{self.index}")
        # if shoot:
        #     self.screen_shot(scene=self.desc) # openvc有点问题，截图暂时先不使用
        element.click()  # 实验下是否可以点击，不可的话可以用下面的方法
        # 另外一种点击方法
        # x, y = element.center()
        # self.driver.click(x, y)
        logger.info(f"successful click 【{self.desc}】"
                    f"{self._kwargs}:index{self.index}")

    def long_click(self, retries=FIND_ELEMENT_RETRY, shoot=True):
        """长按"""
        element = self.find_element(retries)
        if not element:
            raise ElementNotFoundError(f"Not found element【{self.desc}】:"
                                       f"{self._kwargs},index:{self.index}")
        # if shoot:
        #     self.screen_shot(scene=self.desc) # openvc有点问题，截图暂时先不使用
        element.long_click()
        logger.info(f"successful long_click 【{self.desc}】"
                    f"{self._kwargs}:index{self.index}")

    def swipe(self, start_x, start_y, end_x, end_y, direction='up', steps=10,
              retries=FIND_ELEMENT_RETRY, shoot=True):
        """滑动
        @param shoot:
        @param retries:
        @param direction:四个方向
        @param start_x:from position
        @param start_y:from position
        @param end_x: from position
        @param end_y: to position
        @param steps:滑动速度
        """
        # 先元素定位再滑动
        element = self.find_element(retries)
        if not element:
            raise ElementNotFoundError(f"Not found element【{self.desc}】:"
                                       f"{self._kwargs},index:{self.index}")
        if direction:
            assert direction in ("left", "right", "up", "down")
            element.swipe(direction=direction, steps=steps)
            # if shoot:
            #     self.screen_shot(scene=self.desc) # openvc有点问题，截图暂时先不使用
            logger.info(f"【{self.desc}】{self._kwargs}:index{self.index}"
                        f"Successfully swipe by {direction}")
        else:
            # 根据坐标点直接滑动
            self.driver.swipe(start_x, start_y, end_x, end_y, steps)
            # if shoot:
            #     self.screen_shot(scene=self.desc) # openvc有点问题，截图暂时先不使用
            logger.info(f"【{self.desc}】{self._kwargs}:index{self.index}"
                        f"Successfully swipe by position")

    def swipe_ext(self, direction="up", scale=0.9):
        """向固定方向滑动UP、DOWN、LEFT、RIGHT"""
        size_x, size_y = self.driver.window_size()
        phone_x = size_x/2
        phone_y = size_y/2
        # 中心点位置开始滑动
        assert direction in ("left", "right", "up", "down")
        if direction == 'up':
            self.swipe(phone_x, phone_y, phone_x, 10)
        if direction == 'down':
            self.swipe(phone_x, phone_y, phone_x, size_y)
        if direction == 'left':
            self.swipe(phone_x, phone_y, 10, phone_y)
        if direction == 'right':
            self.swipe(phone_x, phone_y, size_x-10, phone_y)
        logger.info(f"page successfully swipe by {direction}")

    def send_keys(self, text='', retries=FIND_ELEMENT_RETRY, shoot=True):
        """输入内容"""
        element = self.find_element(retries)
        if not element:
            raise ElementNotFoundError(f"Not found element【{self.desc}】:"
                                       f"{self._kwargs},index:{self.index}")
        # if shoot:
        #     self.screen_shot(scene=self.desc) # openvc有点问题，截图暂时先不使用
        element.send_text(text=text) if self.xpath else \
            element.send_keys(text=text)
        logger.info(f"【{self.desc}】{self._kwargs}{self.index}"
                    f"Successfully send_keys {text}")

    def get_text(self, retires=FIND_ELEMENT_RETRY):
        element = self.find_element(retires)
        if not element:
            raise ElementNotFoundError(f"Not found element【{self.desc}】:"
                                       f"{self._kwargs},index:{self.index}")

        logger.info(f"【{self.desc}】{self._kwargs}{self.index}"
                    f"Successfully send_keys")
        return element.get_text()

    def open_scheme(self, url=''):
        """adb shell am start -a android.intent.action.VIEW -d url"""
        self.driver.open_url(url=url)

    def app_start(self):
        """启动app"""
        self.driver.screen_on()
        logger.info("start app")
        self.driver.app_start(test_package)

    def app_stop(self):
        """停止APP"""
        logger.info("kill app")
        self.driver.app_stop(test_package)

    def set_phone_proxy(self, host="", port=""):
        """设置代理
        @rtype: object
        @param host: 主机地址
        @param port: 端口号
        """
        logger.info("设置手机代理")
        # os.system(f"adb shell setting put global http_proxy{host}:{port}")
        self.driver.shell(f"adb shell setting put global http_proxy"
                          f"{host}:{port}")

    def delete_proxy(self):
        """删除代理"""
        logger.info("清除手机代理")
        # os.system("adb shell settings delete global http_proxy")
        # os.system("adb shell settings delete global global_http_proxy_host")
        # os.system("adb shell settings delete global global_http_proxy_port")
        self.driver.shell("adb shell settings delete global http_proxy")
        self.driver.shell("adb shell settings delete global "
                          "global_http_proxy_host")
        self.driver.shell("adb shell settings delete global "
                          "global_http_proxy_port")
        # 重启设备
        # os.system("adb reboot")

    def screen_shot(self, scene=None):
        """截取当前场景图片和元素图片,并保存结果"""
        current_photo = self.driver.screenshot(f"{scene}.png")
        # 获取当前元素4点坐标
        bounds = self.find_element().info.get('bounds')
        pos_x = (bounds['top']+bounds['bottom'])/2
        pos_y = (bounds['left']+bounds['right'])/2
        src = cv2.imread(current_photo)
        color = (0, 0, 255)
        draw_maker = cv2.drawMarker(src, (pos_x, pos_y), color,
                                    cv2.MARKER_SQUARE,
                                    thickness=3)
        # 保存原图片
        with open(f"/Users/apple/Desktop/UiautoTest/photo/", 'W') as f:
            f.write(current_photo)
            f.close()
        # 保存标记后的图片
        file_name = f"../photo/{scene}1.png"
        cv2.imwrite(file_name, draw_maker)



