#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import platform
import time
import datetime
import subprocess
import optparse
import shlex

import sched

__author__ = 'sinlov'

is_verbose = False
schedule = sched.scheduler(time.time, time.sleep)

"""
default max time 1 hour 
"""
max_time = 60 * 60

root_run_path = os.getcwd()
"""
default exec time out 1 second
"""
out_of_time_default = 60 * 1


class PLog:
    def __init__(self):
        pass

    RUNTIME_VERSION_ERROR = """
        This script must run python 2.6.+
        """

    ERROR = '\033[91m'
    OK_GREEN = '\033[96m'
    WARNING = '\033[93m'
    OK_BLUE = '\033[94m'
    HEADER = '\033[95m'
    WRITE = '\033[98m'
    BLACK = '\033[97m'
    END_LI = '\033[0m'

    @staticmethod
    def check_runtime():
        PLog.log('Python version %s' % platform.python_version(), 'd')
        version_split = platform.python_version().split('.')
        if version_split[0] != '2':
            PLog.log(PLog.RUNTIME_VERSION_ERROR, 'e', True)
            exit(1)
        if version_split[1] < '6':
            PLog.log(PLog.RUNTIME_VERSION_ERROR, 'e', True)
            exit(1)

    @staticmethod
    def log_normal(info):
        print PLog.WRITE + info + PLog.END_LI

    @staticmethod
    def log_assert(info):
        print PLog.BLACK + info + PLog.END_LI

    @staticmethod
    def log_info(info):
        print PLog.OK_GREEN + info + PLog.END_LI

    @staticmethod
    def log_debug(info):
        print PLog.OK_BLUE + info + PLog.END_LI

    @staticmethod
    def log_warning(info):
        print PLog.WARNING + info + PLog.END_LI

    @staticmethod
    def log_error(info):
        print PLog.ERROR + info + PLog.END_LI

    @staticmethod
    def log(msg, lev=str, must=False):
        # type: (str, str, bool) -> None
        if is_verbose or must:
            if not platform.system() == "Windows":
                if lev == 'i':
                    PLog.log_info('%s' % msg)
                elif lev == 'd':
                    PLog.log_debug('%s' % msg)
                elif lev == 'w':
                    PLog.log_warning('%s' % msg)
                elif lev == 'e':
                    PLog.log_error('%s' % msg)
                elif lev == 'a':
                    PLog.log_assert('%s' % msg)
                else:
                    PLog.log_normal('%s' % msg)
            else:
                print ('%s\n' % msg)


def is_platform_windows():
    sys_str = platform.system()
    if sys_str == "Windows":
        return True
    else:
        return False


def find_now_time_format(format_time=str):
    # type: (str) -> str
    """获取当前时间格式化的函数
    :param format_time:
    格式化参数:
      %y 两位数的年份表示（00-99）
      %Y 四位数的年份表示（000-9999）
      %m 月份（01-12）
      %d 月内中的一天（0-31）
      %H 24小时制小时数（0-23）
      %I 12小时制小时数（01-12）
      %M 分钟数（00=59）
      %S 秒（00-59）
      %a 本地简化星期名称
      %A 本地完整星期名称
      %b 本地简化的月份名称
      %B 本地完整的月份名称
      %c 本地相应的日期表示和时间表示
      %j 年内的一天（001-366）
      %p 本地A.M.或P.M.的等价符
      %U 一年中的星期数（00-53）星期天为星期的开始
      %w 星期（0-6），星期天为星期的开始
      %W 一年中的星期数（00-53）星期一为星期的开始
      %x 本地相应的日期表示
      %X 本地相应的时间表示
      %Z 当前时区的名称
      %% %号本身

    :return: time string
    """
    return time.strftime(format_time, time.localtime(time.time()))


def execute_cli(cli_string, cwd=None, timeout=None, is_shell=False, is_info=False):
    """执行一个SHELL命令
        封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
        如果没有指定标准输出和错误输出的管道，因此会打印到屏幕上
        另外的，可以通过返回的 returncode 来判断是否成执行


        支持超时原理：
            subprocess.poll()方法：检查子进程是否结束了，如果结束了
            设定并返回码，放在subprocess.returncode变量中
    参数:
      :param cli_string 运行命令字符串
      :param cwd 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
      :param timeout 超时时间，秒，支持小数，精度0.1秒，默认不输入无超时
      :param is_shell 是否通过shell运行,使用 shlex.split 来解析
      :param is_info 是否同时打印输出
    :return: return class Popen(object)
    :raises: Exception: 执行超时
    """
    if is_shell:
        cmd_string_list = cli_string
    else:
        cmd_string_list = shlex.split(cli_string)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    sub = subprocess.Popen(cmd_string_list, cwd=cwd,
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=is_shell,
                           bufsize=4096)
    while sub.poll() is None:
        if is_info:
            print sub.stdout.readline(),
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception('Timeout：%s' % cli_string)
    return sub


def exec_cli(cmd_string, cwd=None, time_out=None, is_shell=False):
    """执行一个SHELL命令
        封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
        默认开启打印执行输出，不可修改
        操时已经使用 max_out_of_time 设置
    参数:
      :param cmd_string 运行命令字符串
      :param cwd 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
      :param time_out 超时时间，秒，支持小数，精度0.1秒，默认不输入 超时使用 max_out_of_time 设置
      :param is_shell 是否通过shell运行,使用 shlex.split 来解析
    :return: return class Popen(object)
    :raises: Exception: 执行超时
    """
    try:
        if time_out is None:
            time_out = out_of_time_default
        PLog.log('\ncli -> %s\ncwd -> %s\ntimeOut -> %s\nis_shell -> %s\n' % (cmd_string, cwd, time_out, is_shell),
                 'i', True)
        command_out = execute_cli(cmd_string, cwd, time_out, is_shell, True)
        if command_out.returncode == 0:
            str_out = "cmd_line success: %s\n%s" % (cmd_string, str(command_out.stdout.read()))
            command_out.stdout.close()
            PLog.log(str_out, 'd')
            return True
        else:
            str_out = "cmd_line fail out: %s\n%s" % (cmd_string, str(command_out.stdout.read()))
            str_err = "cmd_line fail: %s\n%s" % (cmd_string, str(command_out.stderr.read()))
            command_out.stdout.close()
            command_out.stderr.close()
            PLog.log('%s\n%s' % (str_out, str_err), 'e', True)
            return False
    except Exception, e:
        PLog.log('cmd_line %s\nError info %s' % (cmd_string, str(e)), 'e', True)
        return False


def func(string1, float1):
    print "now is", time.time(), " | output=", string1, float1


def git_pull():
    PLog.log("=> git pull time {0}".format(find_now_time_format("%Y-%m-%d-%H_%M_%S")), 'i')
    cmd_line = 'git pull'
    git_pull_res = exec_cli(cmd_line, root_run_path)
    # if not git_pull_res:
    #     exit(1)
    pass


def job_auto_git_pull(each_time):
    if each_time <= 0:
        PLog.log('each time must gather then 0', 'e', True)
        exit(1)
    PLog.log("start autoPull max_time -> {0}s, each_time -> {1}s".format(max_time, each_time), 'i', True)
    for each in range(max_time):
        if each > 0 and each % each_time == 0:
            PLog.log("schedule.enter time {0}".format(each), 'd')
            schedule.enter(each, 0, git_pull, ())
    schedule.run()


if __name__ == '__main__':
    PLog.check_runtime()
    if len(sys.argv) < 2:
        print "You must input params or see -h"
        exit(1)
    check_p = str(sys.argv[1])
    if not check_p.startswith('-'):
        print 'You params is error please see -h'
        exit(1)
    parser = optparse.OptionParser('Usage %prog ' + '-i -v')
    parser.add_option('-v', '--verbose', dest='v_verbose', action="store_true",
                      help="see verbose", default=False)
    parser.add_option('--max', dest='max_time', type="string",
                      help="set max time of scm job use second"
                      , metavar="3600")
    parser.add_option('--autoPull', dest='auto_pull', type="string",
                      help="auto run git pull by time second"
                      , metavar="60")
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    try:
        if options.max_time:
            max_time = int(options.max_time)
            if max_time < 1:
                PLog.log('max_time must gather then 0', 'e', True)
                exit(1)
        if options.auto_pull:
            job_auto_git_pull(int(options.auto_pull))
        else:
            PLog.log("not set any scm job, please check", 'e', True)
    except Exception as e:
        PLog.log("error {0}".format(str(e)), 'e', True)
        pass
