# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:config.py
@CreateTime:2022/6/26 16:23
"""

import yaml
FIND_ELEMENT_RETRY = 3


def read_yaml():
    """读取基础配置"""
    with open("./config.yaml", 'rb') as f:
        my_config = yaml.safe_load(f)
        return my_config






