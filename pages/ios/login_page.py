# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:login_page.py
@CreateTime:2022/9/12 16:37
"""
import time

from base.config import read_yaml
from base.ios.ios_base import IosBase
user_name = read_yaml().get("username")
password = read_yaml().get("password")
package_name = read_yaml().get("package1")


class LoginPage(IosBase):
    """登录页面"""
    privacy_button = IosBase(nameContains='我已阅读并同意', annotations='用户协议')
    other_login = IosBase(value='以其他方式登录', annotations='以其他方式登录')

    @property
    def get_app_type(self):
        _app_type = None
        if package_name.__contains__('gifshow'):
            _app_type = 'kwai'
        if package_name.__contains__('nebula'):
            _app_type = 'nebula'
        return _app_type

    def login(self):
        url = 'kwai://settings' if self.get_app_type == 'kwai' else \
            'ksnebula://settings'
        self.open_schema(url)
        time.sleep(5)
        # x, y = self.privacy_button.bounds()
        self.privacy_button.click()
        self.other_login.click()

        pass
