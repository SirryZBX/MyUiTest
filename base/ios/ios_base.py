# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:ios_base.py
@CreateTime:2022/8/28 11:54
"""
import inspect

import cv2
from base.ios.ios_device import IosTiDevice, retry_connect_wda
import time
from base.config import read_yaml
from base.config import FIND_ELEMENT_RETRY
from base.error import ElementNotFoundError
from base.my_logger import logger
from wda import Element
p_name = read_yaml().get('package1')


class IosBase(object):
    """ios测试框架"""
    def __init__(self, *args, **kwargs):
        """初始化"""
        self._kwargs = kwargs
        self.className = kwargs.get('className', '')
        self.name = kwargs.get('name', '')
        self.label = kwargs.get('label', '')
        self.labelContains = kwargs.get('labelContains', '')
        self.value = kwargs.get('value', '')
        self.valueContains = kwargs.get('valueContains', '')
        self.xpath = kwargs.get('xpath', '')
        self.text = kwargs.get('text', '')
        self.nameContains = kwargs.get('nameContains','')

        self.index = kwargs.pop('index', 0)
        self.annotations = kwargs.pop('annotations', '')

        # 初始化tidives
        self.device = IosTiDevice()
        self.serialno = self.device.serialno
        self._element: Element = None

    @retry_connect_wda
    def find_element(self, retries=FIND_ELEMENT_RETRY, timeout=20):
        """查找元素
        @param timeout: 查找元素的超时时间
        @type retries: 查找元素的重试次数
        """
        logger.info(f'{self.serialno} find element {self.annotations}:'
                    f'{self._kwargs}')
        _element = None
        selector = self.device.client(**self._kwargs)
        while True:
            _element: Element = selector.get(timeout=timeout)
            if _element:
                self._element = _element
                break
            if retries > 0:
                logger.warning(f'{self.serialno} Retry found element '
                               f'{self.annotations}:{self._kwargs}')
                retries -= 1
                time.sleep(1)
            if retries < 0:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)  # 返回调用者信息
                logger.warning(f'【{caller.function}:{caller.lineno}】Not found '
                               f'element{self.annotations}:{self._kwargs}')
                break
        return _element

    @retry_connect_wda
    def find_element_by_swipe(self, retries=FIND_ELEMENT_RETRY, timeout=20):
        """滑动查找用户,暂时用不到，后边再补吧"""
        pass

    def bounds(self):
        """定制一个小圆圈要点击的左上角坐标"""
        element = self.find_element()
        bounds = self._element.bounds
        left_x = bounds.x + 20
        left_y = bounds.y
        return left_x, left_y

    @retry_connect_wda
    def click(self, retries=FIND_ELEMENT_RETRY, timeout=20, shoot=True):
        """点击"""
        _element = self.find_element(retries=retries, timeout=timeout)
        x, y = self.bounds()
        if not _element:
            raise ElementNotFoundError(f'{self.serialno} Not found element'
                                       f'{self}')
        # if shoot:
        #     self.screen_shot(scene=self.annotations)  # 暂时还不能用
        self.device.client.click(x, y)
        # _element.click()
        logger.info(f'{self.serialno} Successful click {self}')

    @retry_connect_wda
    def set_text(self, value, retries=FIND_ELEMENT_RETRY, timeout=20,
                 shoot=True,):
        """输入"""
        _element = self.find_element(retries, timeout)
        if not _element:
            raise ElementNotFoundError(f'{self.serialno} Not found element'
                                       f'{self}')
        # if shoot:
        #     self.screen_shot(scene=self.annotations)
        _element.set_text(value)

    @retry_connect_wda
    def click_if_exist(self, retries=FIND_ELEMENT_RETRY, timeout=20, shoot=True):
        """当元素存在时点击"""
        _element = self.find_element(retries, timeout)
        if not _element:
            return False
        if shoot:
            self.screen_shot(scene=self.annotations)
        _element.click()
        return True

    @retry_connect_wda
    def app_stop(self):
        self.device.client.app_terminate(p_name)

    def open_schema(self, url):
        self.open_schema_safair(url)

    @retry_connect_wda
    def open_schema_safair(self, url):
        """利用手机自带safari打开url"""
        # self.device.client.home()
        self.device.client.app_start('com.apple.mobilesafari')
        # _s = self.device.client.session('com.apple.mobilesafari')
        # _s(name='URL', label='地址').click()
        logger.info('输入快链')
        IosBase(name='URL', value='搜索或输入网站名称').set_text(url)
        IosBase(label='前往').click()
        # self.device.client(name='URL', value='搜索或输入网站名称').get().set_text(url)
        logger.info('输入成功')
        # self.device.client(label='前往').click()
        time.sleep(1)
        self.device.client(name='打开').click_exists()

    def screen_shot(self, scene=None):
        """截取当前场景图片和元素图片,并保存结果"""
        file_name = f'../photo/{time.time()}'
        current_photo = self.device.client.screenshot(f"{scene}.png")
        # 获取当前元素4点坐标
        bounds = self.find_element().info.get('bounds')
        pos_x = int((bounds['top']+bounds['bottom'])/2)
        pos_y = int((bounds['left']+bounds['right'])/2)
        src = cv2.imread(current_photo)
        color = (0, 0, 255)
        draw_maker = cv2.drawMarker(src, (pos_x, pos_y), color,
                                    cv2.MARKER_SQUARE,
                                    thickness=3)
        # 保存原图片
        with open(file_name, 'W') as f:
            f.write(current_photo)
            f.close()
        # 保存标记后的图片
        cv2.imwrite(file_name, draw_maker)














