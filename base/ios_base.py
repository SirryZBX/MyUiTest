# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:ios_base.py
@CreateTime:2022/8/28 11:54
"""
import wda
from ios_device import IosTiDevice
import time
from .config import read_yaml
from config import FIND_ELEMENT_RETRY


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

        self.index = kwargs.pop('index', 0)
        self.annotations = kwargs.pop('annotations', '')
        self.p_name = read_yaml().get('package1')
        # 初始化tidives
        self.device = IosTiDevice()
        # 初始化wda
        self.c = wda.Client('http://localhost:8200')
        self.driver = self.c.session(f'{self.p_name}')

    def find_element(self, retries=FIND_ELEMENT_RETRY, timeout=20):
        """查找元素"""
        pass











