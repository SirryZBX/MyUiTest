# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:error.py
@CreateTime:2022/7/17 14:45
"""


class BaseError(Exception):
    """异常类"""
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return repr(self.text)


class ElementNotFoundError(BaseError):
    """元素未找到报错，后续报错待补充"""
    pass




