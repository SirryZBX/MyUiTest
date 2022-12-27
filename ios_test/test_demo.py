# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:test_demo.py
@CreateTime:2022/9/15 21:20
"""
from pages.ios.login_page import LoginPage
import pytest


class TestDemo:

    def test_login(self):
        LoginPage().login()


if __name__ == "__main__":
    pytest.main(['-s', '-q', 'test_demo.py'])
