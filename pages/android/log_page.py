# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:log_page.py
@CreateTime:2022/7/2 16:22
"""
import time

from base.base_action import BaseAction
import pytest
from base.config import read_yaml
from base.base_action import logger

user_name = read_yaml().get("username")
password = read_yaml().get("password")
package_name = read_yaml().get("package")


class LogPage(BaseAction):
    """登录页面"""

    button_login_left = BaseAction(resourceId="com.smile.gifmaker:id/left_text",
                                   text="登录", desc='首页登录按钮')
    phone_label = BaseAction(resourceId="com.smile.gifmaker:id/phone_et",
                             desc="手机号输入框")
    button_password = BaseAction(resourceId="com.smile.gifmaker:"
                                            "id/switch_login_way",
                                 desc="切换密码登录按钮")
    password_label = BaseAction(resourceId="com.smile.gifmaker:id/password_et",
                                desc="密码输入框")
    button_login = BaseAction(resourceId="com.smile.gifmaker:id/confirm_btn",
                              desc="登录按钮点击")
    button_other = BaseAction(resourceId="com.smile.gifmaker:"
                                         "id/btn_other_login_ways",
                              desc="其他方式登录")
    button_other_phone = BaseAction(resourceId="com.smile.gifmaker:"
                                               "id/btn_other_login_ways",
                                    text="其他手机号码登录", desc="其他手机号")
    button_phone_login = BaseAction(resourceId="com.smile.gifmaker:"
                                               "id/btn_other_login_ways",
                                    text="手机号码登录", desc="手机号码登录按钮")
    agree_button = BaseAction(resourceId="com.smile.gifmaker:"
                                         "id/protocol_checkbox", desc="同意协议")
    phone_delete_button = BaseAction(resourceId="com.smile.gifmaker:id/"
                                                "remove_phone_num_btn",
                                     desc="删除手机号")

    @staticmethod
    def get_app_type():
        _app_type = None
        if package_name.__contains__('gifmaker'):
            _app_type = 'kwai'
        if package_name.__contains__('nebula'):
            _app_type = 'nebula'
        if not _app_type:
            raise ValueError('No app_type matches')
        return _app_type

    def login(self):
        """登录"""
        self.app_stop(package_name)
        url = "kwai://myprofile" if self.get_app_type() == 'kwai' else \
            'ksnebula://myprofile'
        self.open_scheme(url)
        if self.button_other.find_element(retries=1, timeout=3):
            self.button_other.click()
        if self.button_other_phone.find_element(retries=1, timeout=3):
            self.button_other_phone.click()
        if self.button_phone_login.find_element(retries=1, timeout=3):
            self.button_phone_login.click()
        if self.phone_delete_button.find_element(retries=1, timeout=3):
            self.phone_delete_button.click()
        self.phone_label.send_keys(user_name)    # 输入手机号
        if self.button_password.find_element(retries=1):
            self.button_password.click()  # 切换到密码登录
        self.password_label.send_keys(password)  # 输入密码
        self.agree_button.click()
        self.button_login.click()  # 登录按钮点击
        time.sleep(2)



