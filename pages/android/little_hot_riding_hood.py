# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:little_hot_riding_hood.py
@CreateTime:2022/8/6 16:30
"""
import time

from base.base_action import BaseAction
import pytest


class LittleHot(BaseAction):
    """小红帽页面"""
    button_cancel = BaseAction(resourceId="com.smile.gifmaker:id/negative",
                               desc="以后再说")
    button_follow = BaseAction(resourceId="com.smile.gifmaker:id/follow_button",
                               index=2, desc="第三个关注按钮")
    button_pencil = BaseAction(xpath='//*[@resource-id="com.smile.gifmaker:'
                                     'id/user_alias_mark"]/'
                                     'android.widget.ImageView[1]', desc="小铅笔")

    button_delete = BaseAction(xpath='//*[@resource-id="com.smile.gifmaker:'
                                     'id/recycler_view"]/android.view.ViewGroup'
                                     '[1]/android.widget.ImageButton[1]',
                               desc="删除按钮")
    user_text = BaseAction(resourceId="com.smile.gifmaker:id/name", desc="全部昵称")
    nickname_label = BaseAction(className="android.widget.FrameLayout",
                                desc="备注名输入框")
    confirm_button = BaseAction(resourceId="com.smile.gifmaker:id/positive",
                                desc="备注名确认")

    def open_little_hot(self):
        self.open_scheme("kwai://explorefriend")

    def follow(self):
        self.button_follow.click()
        assert self.button_pencil.find_element(retries=1, timeout=3)

    def delete(self):
        old_text = self.user_text.get_text()[0]
        self.button_delete.click()
        new_text = self.user_text.get_text()[0]
        assert not old_text == new_text

    def change_nickname(self, text=""):
        self.button_pencil.click()
        self.driver.send_keys(text)
        time.sleep(1)
        self.confirm_button.click()
        assert self.user_text.get_text()[2] != text


