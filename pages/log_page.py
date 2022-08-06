# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:log_page.py
@CreateTime:2022/7/2 16:22
"""

from base.base_action import BaseAction


class LogPage(BaseAction):
    """登录页面"""

    button_login = BaseAction(resourceId="", text="", desc='登录按钮')

    def login(self, username, password):
        """登录"""
        pass


