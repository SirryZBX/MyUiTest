# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:my_logger.py
@CreateTime:2022/7/10 17:48
"""

import logging
import time


class MyLogging(logging.Logger):
    def __init__(self, name, level=logging.INFO, file=None, hint_show=True):
        """

        :param name: 日志名字
        :param level: 级别
        :param file: 日志文件名称
        :param hint_show: 日志控制台提示(默认为True 自动开启)
        """
        # 继承logging模块中的Logger类，因为里面实现了各种各样的方法，很全面，但是初始化很简单
        # 所以我们需要继承后把初始化再优化下，变成自己想要的。
        super().__init__(name, level)

        # 设置日志格式
        fmt = "%(asctime)s %(name)s %(levelname)s " \
              "执行程序名:%(filename)s--%(lineno)d行 :%(message)s"

        # %(levelno)s：打印日志级别的数值
        # %(levelname)s：打印日志级别的名称
        # %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
        # %(filename)s：打印当前执行程序名
        # %(funcName)s：打印日志的当前函数
        # %(lineno)d：打印日志的当前行号
        # %(asctime)s：打印日志的时间
        # %(thread)d：打印线程ID
        # %(threadName)s：打印线程名称
        # %(process)d：打印进程ID
        # %(message)s：打印日志信息
        formatter = logging.Formatter(fmt)

        # 文件输出渠道
        if file:
            handle2 = logging.FileHandler(file, encoding="utf-8")
            handle2.baseFilename = file
            handle2.setFormatter(formatter)
            self.addHandler(handle2)

            # 控制台渠道
            if hint_show:
                handle1 = logging.StreamHandler()
                handle1.setFormatter(formatter)
                self.addHandler(handle1)


logger = MyLogging(name='测试', level=logging.INFO,
                   file=f"../current_log/{time.time()}.txt", hint_show=True)




