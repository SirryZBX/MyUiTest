# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:ios_device.py
@CreateTime:2022/9/10 20:30
"""
import binascii
import time
from functools import cached_property

import requests

from base.config import read_yaml
import os
import subprocess
import wda

from base.error import WDAMaxRetryError
from base.my_logger import logger
from base.ios.ios_wda import IosWda
wda.DEBUG = True
wda.DEVICE_WAIT_TIMEOUT = 30
wda.HTTP_TIMEOUT = 180
wda_retry_times = 30


def retry_connect_wda(fun):
    """wda"""
    def wrapper(self, *args, **kwargs):
        return _inner_retry_connect_wda(self, fun, *args, **kwargs)

    return wrapper


def _inner_retry_connect_wda(self, fun, *args, **kwargs):
    global wda_retry_times
    while wda_retry_times > 0:
        try:
            return fun(self, *args, **kwargs)
        except (requests.exceptions.ConnectionError, binascii.Error)as e:
            logger.debug(e)
            logger.warning(f'wda error,{wda_retry_times} retry')
            w = IosWda()
            w.launch_wda()
            wda_retry_times -= 1
    if wda_retry_times == 0:
        raise WDAMaxRetryError('')


class IosTiDevice(IosWda):
    """tidevice启动服务封装"""
    def __init__(self):
        super().__init__()
        self.package = read_yaml().get('package1')

    @cached_property
    def client(self):
        """启动tidevice服务"""
        logger.info('start set up wda')
        return wda.Client()

    @cached_property
    def session(self):
        return self.client.session(f'{self.package}')






