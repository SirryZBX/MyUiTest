# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:test_PYMK.py
@CreateTime:2022/6/26 16:37
"""
import time

import pytest
import allure
from pages.log_page import LogPage
from pages.little_hot_riding_hood import LittleHot
import os


@allure.feature("测试PYMK-小红帽页面")
class TestCase:
    """测试用例"""

    @allure.story("登录")
    @pytest.fixture(scope="class")
    def test_login(self):
        LogPage().login()

    @allure.story("测试小红帽页的功能")
    def test_little_hot_pymk(self, test_login):
        with allure.step("通过快链进入小红帽页"):
            LittleHot().open_little_hot()
        with allure.step("点击第三个用户的关注按钮"):
            LittleHot().follow()
            time.sleep(2)
        with allure.step("修改备注名"):
            LittleHot().change_nickname('abc')
        with allure.step("删除第一个元素"):
            LittleHot().delete()


if __name__ == "__main__":
    pytest.main(['-s', '-q', 'test_PYMK.py', '--clean-alluredir',
                 '--alluredir=allure-results'])
    os.system(r"allure generate -c -o allure-report")


