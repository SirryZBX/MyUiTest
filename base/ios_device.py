# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:ios_device.py
@CreateTime:2022/9/10 20:30
"""
from config import read_yaml
import os


class IosTiDevice(object):
    """tidevice启动服务封装"""
    def __init__(self):
        self.bundle_id = read_yaml().get('bundle_id')
        self.device_id = read_yaml().get('device_id')

    def start_tidevice(self):
        """启动tidevice服务"""
        os.system(f'tidevice{self.device_id} wdaproxy -B '
                  f'{self.bundle_id} --port 8200')



