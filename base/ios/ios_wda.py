# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:ios_wda.py
@CreateTime:2022/9/17 17:18
"""
import datetime
import time

from base.error import WDALaunchFailError
from base.my_logger import logger
from requests import request
from base.config import read_yaml
from retry import retry
from base import shell
# import httpdo
import os
import re
BASE_DIR = os.getcwd()
WDA_LOG = os.path.join(BASE_DIR, 'wda_log')


def http_res(method, url, **kwargs):
    """返回接口响应的json数据"""
    r = request(method, url, **kwargs)
    res = r.json()
    return res


def is_wda_running():
    """判断wda是否运行"""
    url = 'http://loaclhost:8100'
    try:
        r = http_res('get', url)
        value = r.get('value')
        if isinstance(value, dict) and value.get('state') == 'success':
            logger.debug(value)
            logger.info(f'WDA is running')
            return True
    except Exception:
        logger.info('WDA disconnect,please retry launch wda')
        return False


def compare_pattern(pattern, list):
    """判断特征值是否在列表中"""
    flag_value = re.compile(pattern)
    for key in list:
        if len(flag_value.findall(key)) > 0:
            return True
    return False


def _get_wda_log(path):
    """获取wda日志信息并返回"""
    res = ''
    with open(path, 'r') as r:
        for line in r.readlines():
            res += line
    return res


class IosWda(object):
    """wda服务"""
    def __init__(self):
        self.serialno = read_yaml().get('device_id')
        self.bundle_id = read_yaml().get('bundle_id')

    def launch_wda(self):
        """启动wda"""
        self.reset_iproxy()  # 重新设置iproxy
        if is_wda_running():
            return True
        wda_launch_cmd = f'tidevice -u {self.serialno} xctest -B ' \
                         f'{self.bundle_id} --debug'
        wda_run_sign = 'WebDriverAgent start successfully'
        flag = self.wait_launch_wda(wda_launch_cmd, wda_run_sign)
        if not flag:
            raise WDALaunchFailError('wda 启动失败了')
        return is_wda_running()

    @retry(tries=3, delay=1)
    def wait_launch_wda(self, cmd, sign, timeout=30):
        start_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        wda_log_path = os.path.join(WDA_LOG, f'wda_{start_time}.log')
        current_time = int(time.time())
        with open(wda_log_path, 'w')as writer, open(wda_log_path, 'r')as reader:
            shell.except_cmd(cmd, out=writer)

            while not compare_pattern(sign, reader.readlines()) \
                    and int(time.time())-current_time < timeout:
                time.sleep(1)
                logger.info('')
                writer.flush()  # 更新文件
                wda_output = reader.readlines()
                if compare_pattern(sign, wda_output):
                    logger.info(f'{self.serialno} launch wda Successfully')
                    return True
        if int(time.time()) - current_time >= timeout:
            logger.warning(f'{self.serialno} launch wda fail,log:'
                           f'{_get_wda_log(wda_log_path)}')
            return False

    def reset_iproxy(self):
        self.stop_iproxy()
        self.start_iproxy()

    def start_iproxy(self):
        cmd = f'tidevice -u {self.serialno} relay 8100 8100'
        shell.except_cmd(cmd)
        time.sleep(2)
        logger.info(f'{self.serialno} Successful iproxy')

    def stop_iproxy(self):
        logger.info(f'{self.serialno} Killing iproxy')
        shell.kill_want_pid('relay', 8100)
        logger.info(f'{self.serialno} Successful Killing iproxy process')

    def stop_wda(self):
        shell.kill_want_pid(f'tidevice', {self.serialno})






