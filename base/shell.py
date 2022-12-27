# -*- coding: UTF-8 -*-
# enve python3.9
"""
@Author:大王
@File:shell.py
@CreateTime:2022/9/17 17:32
"""
import shlex
import subprocess
from base.my_logger import logger
import psutil


def except_cmd(cmd, out=subprocess.PIPE, shell=False):
    """执行shell命令"""
    logger.info(cmd)
    if isinstance(cmd, str) and not shell:
        cmd = shlex.split(cmd)
    if isinstance(cmd, list):
        shell = False
    return subprocess.Popen(cmd, stdout=out, stderr=out,
                            shell=shell)


def get_output(cmd):
    """执行命令，并拿到执行的结果"""
    logger.info(cmd)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return output.decode()  # 需要解码


def kill_pid(pid):
    """杀死进程"""
    try:
        p = psutil.Process(pid=pid)
        p.kill()
    except psutil.NoSuchProcess:
        logger.info(f'No Such Process{pid}')


def kill_want_pid(*args):
    """杀死当前想要干掉的进程"""
    progress = find_pid_by_cmdline_key(*args)  # 进程
    logger.debug(f'f kill {args} pid:{progress}')
    for p in progress:
        kill_pid(p.get('pid'))


def find_pid_by_cmdline_key(*args):
    """通过获取计算机进程对比得到pid"""
    res = []
    for p in psutil.process_iter():
        try:
            cmdline = p.cmdline()
            ret = []
            for cmd in cmdline:
                for key in list(args):
                    if str(key) in cmd:
                        ret.append(key)
                        break
            if len(ret) == len(args):
                res.append({'pid': {p.pid}, 'detail': cmdline})
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            logger.info('')
    return res









# # for p in psutil.process_iter(['pid']):
# #     try:
# #         cmdline = p.cmdline()
# #         print(cmdline)
# #     except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
# #         print("错误")
# #
# # # print(psutil.cpu_times())
# date = subprocess.check_output('ls', shell=True)
# # print(date.decode())