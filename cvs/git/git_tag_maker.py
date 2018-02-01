# -*- coding: utf-8 -*-
import json
import os
import sys
import inspect
import platform
import stat
import time
import datetime
import shlex
import subprocess
import shutil
import re

import logging
import logging.handlers
import getpass

import optparse

__author__ = 'sinlov'

reload(sys)
sys.setdefaultencoding('utf-8')

is_verbose = False
root_run_path = os.getcwd()
this_tag = 'build_'
log_folder = 'log'

"""
自动清空日志的时间差，默认为一周
"""
out_of_time_log_auto_clean = 60 * 60 * 24 * 7

"""
执行默认超时时间 60 * 1 秒
"""
out_of_time_default = 60 * 1
"""
执行单位克隆超时时间 60 * 30 秒
"""
out_of_time_clone = 60 * 30
"""
执行单位推送超时时间 60 * 20 秒
"""
out_of_time_push = 60 * 20

is_force = False
mode_test = False


class Logger_Print:
    ERROR = '\033[91m'
    OK_GREEN = '\033[96m'
    WARNING = '\033[93m'
    OK_BLUE = '\033[94m'
    HEADER = '\033[95m'
    WRITE = '\033[98m'
    BLACK = '\033[97m'
    END_LI = '\033[0m'

    @staticmethod
    def log_normal(info):
        print Logger_Print.WRITE + info + Logger_Print.END_LI

    @staticmethod
    def log_assert(info):
        print Logger_Print.BLACK + info + Logger_Print.END_LI

    @staticmethod
    def log_info(info):
        print Logger_Print.OK_GREEN + info + Logger_Print.END_LI

    @staticmethod
    def log_debug(info):
        print Logger_Print.OK_BLUE + info + Logger_Print.END_LI

    @staticmethod
    def log_warning(info):
        print Logger_Print.WARNING + info + Logger_Print.END_LI

    @staticmethod
    def log_error(info):
        print Logger_Print.ERROR + info + Logger_Print.END_LI


def init_logger(first_tag, sec_tag=str):
    global logger
    log_file = first_tag + sec_tag + '.log'
    log_path = check_current_log_path_and_auto_clean()
    log_path_join = os.path.join(log_path, log_file)
    handler = logging.handlers.RotatingFileHandler(log_path_join, maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger(str(getpass.getuser()))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def init_logger_by_time(tag=str):
    # type: (str) -> Logger
    return init_logger(tag, find_now_time_format('%Y_%m_%d_%H_%M_%S'))


def log_printer(msg, lev=str, must=False):
    # type: (str, str, bool) -> None
    if is_verbose or must:
        if not is_platform_windows():
            if lev == 'i':
                Logger_Print.log_info('%s' % msg)
            elif lev == 'd':
                Logger_Print.log_debug('%s' % msg)
            elif lev == 'w':
                Logger_Print.log_warning('%s' % msg)
            elif lev == 'e':
                Logger_Print.log_error('%s' % msg)
            elif lev == 'a':
                Logger_Print.log_assert('%s' % msg)
            else:
                print '%s\n' % msg
        else:
            print '%s\n' % msg
    if lev == 'i':
        logger.info(msg)
    elif lev == 'd':
        logger.debug(msg)
    elif lev == 'w':
        logger.warning(msg)
    elif lev == 'e':
        logger.error(msg)
    elif lev == 'a':
        logger.debug(msg)
    else:
        logger.info(msg)


def find_now_time_format(format_time=str):
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


def check_current_log_path_and_auto_clean():
    """
    自动在脚本的运行目录创建 log 子目录，并检查日志文件，自动删除一周前的日志
    :return:
    """
    log_path = os.path.join(current_file_directory(), log_folder)
    if not check_dir_or_file_is_exist(log_path):
        os.makedirs(log_path)
    else:
        check_time = time.time()
        for walk_dir, walk_folder, walk_file in os.walk(log_path):
            for f in walk_file:
                if f.endswith('.log'):
                    check_path_join = os.path.join(walk_dir, f)
                    m_time = os.path.getmtime(check_path_join)
                    if check_time - m_time > out_of_time_log_auto_clean:
                        os.remove(check_path_join)
                        print 'auto_clean log file : %s' % check_path_join
    return log_path


def current_file_directory():
    """
    获取脚本文件执行目录
    :return:
    """
    path = os.path.realpath(sys.path[0])  # interpreter starter's path
    if os.path.isfile(path):  # starter is excutable file
        path = os.path.dirname(path)
        return os.path.abspath(path)  # return excutable file's directory
    else:  # starter is python script
        caller_file = inspect.stack()[1][1]  # function caller's filename
        return os.path.abspath(os.path.dirname(caller_file))  # return function caller's file's directory


def is_platform_windows():
    sys_str = platform.system()
    if sys_str == "Windows":
        return True
    else:
        return False


def check_dir_or_file_is_exist(abs_path=str):
    return os.path.exists(abs_path)


def change_files_write(path=str):
    # type: (str) -> None
    for root, dirs, files in os.walk(path):
        for name in files:
            os.chmod(os.path.join(root, name), stat.S_IWRITE)
    logger.info('change change_files_write success')


def del_dot_head_files(path=str):
    try:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.startswith("."):
                    os.remove(os.path.join(root, name))
        logger.info("delete path " + path + " success!")
    except Exception, e:
        logger.error(e)
        print e


def replace_text(t_file=str, s_str=str, r_str=str):
    # type: (str, str, str) -> None
    try:
        lines = open(t_file, 'r').readlines()
        f_len = len(lines) - 1
        for i in range(f_len):
            if s_str in lines[i]:
                lines[i] = lines[i].replace(s_str, r_str)
        open(t_file, 'w').writelines(lines)
        logger.info('replace text success | path: ' + t_file + ' |from: ' + s_str + ' |to: ' + r_str)
    except Exception, e:
        logging.error(e)
        print e


def replace_text_reg(t_file=str, reg_str=str, r_str=str):
    # type: (str, str, str) -> None
    try:
        lines = open(t_file, 'r').readlines()
        f_len = len(lines) - 1
        for i in range(f_len):
            if re.match(reg_str, lines[i]):
                lines[i] = lines[i].replace(lines[i], r_str)
        open(t_file, 'w').writelines(lines)
        logger.info('replace text success | path: ' + t_file + ' |reg: ' + reg_str + ' |to: ' + r_str)
    except Exception, e:
        logging.error(e)
        print e


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
        log_printer('\ncli -> %s\ncwd -> %s\ntimeOut -> %s\nis_shell -> %s\n' % (cmd_string, cwd, time_out, is_shell),
                    'i', True)
        command_out = execute_cli(cmd_string, cwd, time_out, is_shell, True)
        if command_out.returncode == 0:
            str_err = "cmd_line success: %s\n%s" % (cmd_string, str(command_out.stdout.read()))
            command_out.stdout.close()
            log_printer(str_err, 'i', True)
            return True
        else:
            str_out = "cmd_line fail out: %s\n%s" % (cmd_string, str(command_out.stdout.read()))
            str_err = "cmd_line fail: %s\n%s" % (cmd_string, str(command_out.stderr.read()))
            command_out.stdout.close()
            command_out.stderr.close()
            log_printer('%s\n%s' % (str_out, str_err), 'e', True)
            return False
    except Exception, e:
        log_printer('cmd_line %s\nError info %s' % (cmd_string, str(e)), 'e', True)
        return False


def read_json_file(js_path=str):
    if not os.path.exists(js_path):
        log_printer("can not find json file, exit!", 'e', True)
        exit(1)
    try:
        with open(js_path, 'r') as load_js:
            js = json.load(load_js)
        return js
    except Exception, e:
        log_printer('Read json file: %s\n%s\nError, exit!' % (js_path, str(e)), 'e', True)
        exit(1)


def exit_by_not_mode_test(error_message=str):
    # type: (str) -> None
    log_printer(error_message, 'e', True)
    if not mode_test:
        exit(1)


def read_json_config(json_path=str):
    # type: (str) -> None
    global is_verbose
    log_printer('Load config path at: %s\n' % config_file_path, 'i', True)
    if not os.path.exists(json_path):
        log_printer("can not find json config, exit!", 'e', True)
        exit(1)
    try:
        with open(json_path, 'r') as load_js:
            config_js = json.load(load_js)
            js_build_path = check_json_by_key(config_js, 'build_path')
            js_build_path = os.path.join(root_run_path, js_build_path)
            if not check_dir_or_file_is_exist(js_build_path):
                os.mkdir(js_build_path)
            build_projects = check_json_by_key(config_js, 'build_projects')
            mode_p = check_json_by_key(config_js, 'mode')
            if mode_p == 'debug':
                is_verbose = True
            else:
                is_verbose = False
            for project in build_projects:
                filter_project_config(project, js_build_path)
    except Exception, e:
        log_printer('Read json config file: %s\n%s\nError, exit!' % (json_path, str(e)), 'e', True)
        exit(1)


def check_json_by_key(json_dir, j_key):
    if j_key in json_dir:
        return json_dir[j_key]
    else:
        exit_by_not_mode_test('not find json key [ %s ] at [ %s ] exit!' % (j_key, json_dir))


def git_clone_project_by_branch_and_try_pull(project_url=str, local_path=str, branch='', tag=''):
    if not branch.strip():
        branch = 'master'
    if check_dir_or_file_is_exist(local_path):
        clone_is_exists = '\n===\nClone project is exist path: \n%s\n===\n' % local_path
        log_printer(clone_is_exists, 'i', True)
        if tag.strip():
            auto_clean_build_project(local_path)
            tag_mode_remove_old_if_exist = '\n===\nBecause config tag so must delete old local path: \n%s\n===\n' % local_path
            log_printer(tag_mode_remove_old_if_exist, 'i', True)
            cmd_line = 'git clone %s -b %s %s' % (project_url, branch, '\"%s\"' % local_path)
            clone_res = exec_cli(cmd_line, root_run_path, out_of_time_clone)
            if not clone_res:
                exit_by_not_mode_test(cmd_line)
            git_tag_checkout = 'git checkout %s' % tag
            clone_res = exec_cli(git_tag_checkout, local_path, out_of_time_clone)
            if not clone_res:
                exit_by_not_mode_test(git_tag_checkout)
    else:
        cmd_line = 'git clone %s -b %s %s' % (project_url, branch, '\"%s\"' % local_path)
        clone_res = exec_cli(cmd_line, root_run_path, out_of_time_clone)
        if not clone_res:
            exit_by_not_mode_test(cmd_line)
        if tag.strip():
            git_tag_checkout = 'git checkout %s' % tag
            clone_res = exec_cli(git_tag_checkout, local_path, out_of_time_clone)
            if not clone_res:
                exit_by_not_mode_test(git_tag_checkout)
    git_branch_check = 'git branch -v'
    exec_cli(git_branch_check, local_path)
    git_fetch = 'git fetch -v'
    exec_cli(git_fetch, local_path)
    gs_cmd = 'git status'
    gs = exec_cli(gs_cmd, local_path)
    if not gs:
        exit_by_not_mode_test(gs_cmd)


def auto_clean_build_project(local=str):
    if not check_dir_or_file_is_exist(local):
        log_printer('Not found path: %s\exit 1' % local, 'e', True)
        exit(1)
    change_files_write(local)
    time.sleep(1)
    shutil.rmtree(local, True)
    time.sleep(1)
    log_printer('Auto clean success path: %s' % local, 'i', True)


def check_project_version_info_by_file(local, version_file=str, version_name=str, version_code=str):
    gp_path = os.path.join(local, version_file)
    if not check_dir_or_file_is_exist(gp_path):
        exit_by_not_mode_test('version_file not found  at path: %s\exit 1' % gp_path)
    has_version_name = False
    has_version_code = False
    gp_file = open(gp_path, 'r')
    gp_content = gp_file.readlines()
    for index, content in enumerate(gp_content):
        if version_name in content:
            log_printer('Find version_name: %s' % content)
            has_version_name = True
        if version_code in content:
            log_printer('Find version_code: %s' % content)
            has_version_code = True
    gp_file.close()
    if has_version_name and has_version_code:
        log_printer('Check version by %s success' % version_file, 'i', True)
        return True
    else:
        exit_by_not_mode_test(
            'Check version by %s fail!\n-> path %s\n'
            '-> version_name check: %s <- want: %s\n'
            '-> version_code check: %s <- want: %s\nExit at ordinary mode' %
            (version_file, gp_path, has_version_name, version_name, has_version_code, version_code))
        return False


def clone_by_tag_or_not_has_tag(branch_p, git_url_p, local_p, project):
    if 'tag' in project.keys():
        tag_p = project['tag']
        git_clone_project_by_branch_and_try_pull(git_url_p, local_p, branch_p, tag_p)
    else:
        git_clone_project_by_branch_and_try_pull(git_url_p, local_p, branch_p)


def git_add_and_commit_by_message(local_p, tag_message):
    cmd_line = 'git add .'
    add_res = exec_cli(cmd_line, local_p, out_of_time_default)
    if not add_res:
        exit(1)
    cmd_line_commit = 'git commit -m "%s"' % tag_message
    add_res = exec_cli(cmd_line_commit, local_p, out_of_time_default)
    if not add_res:
        exit(1)


def check_version_file_when_has_version_check(local_p, project):
    if 'version_check' in project.keys():
        version_check_p = project['version_check']
        version_file = check_json_by_key(version_check_p, 'version_file')
        version_name = check_json_by_key(version_check_p, 'version_name')
        version_code = check_json_by_key(version_check_p, 'version_code')
        by_file = check_project_version_info_by_file(local_p, version_file, version_name, version_code)
        return by_file
    else:
        return True


def run_tag_file_tasks_if_has(local_p, project):
    if 'tag_file_tasks' in project.keys():
        tag_file_tasks = project['tag_file_tasks']
        for file_task in tag_file_tasks:
            task_name = check_json_by_key(file_task, 'name')
            path_file = check_json_by_key(file_task, 'file')
            file_from = check_json_by_key(file_task, 'from')
            file_to = check_json_by_key(file_task, 'to')
            abs_task_path = os.path.join(local_p, path_file)
            if not check_dir_or_file_is_exist(abs_task_path):
                exit_by_not_mode_test('can not find tag_file_task file at [ %s ]' % abs_task_path)
            else:
                log_printer('try to do tag_file_task\n-> Name: -> %s\n-> File: %s\n-> from: %s\n-> to: %s' %
                            (task_name, abs_task_path, file_from, file_to), 'i', True)
                replace_text(abs_task_path, file_from, file_to)


def remove_tags_local(local_p, tag_git):
    if 'remove_local_tags' in tag_git.keys():
        remove_local_tags = check_json_by_key(tag_git, 'remove_local_tags')
        if len(remove_local_tags) < 1:
            log_printer('remove_local_tags size less than 1 at %s exit!' % tag_git, 'e', True)
            exit(1)
        for remove_local_tag in remove_local_tags:
            tag_name = check_json_by_key(remove_local_tag, 'tag_name')
            if tag_name == '':
                log_printer('remove_tags_local [ tag_name ] is "" so pass\n', "w", True)
            else:
                cmd_line = 'git tag -d %s' % tag_name
                remove_tag_res = exec_cli(cmd_line, local_p, out_of_time_default)
                if not remove_tag_res:
                    exit(1)


def remove_tags_origin(local_p, tag_git):
    if 'remove_origin_tags' in tag_git.keys():
        remove_origin_tags = check_json_by_key(tag_git, 'remove_origin_tags')
        if len(remove_origin_tags) < 1:
            log_printer('remove_origin_tags size less than 1 at %s exit!' % tag_git, 'e', True)
            exit(1)
        for remove_local_tag in remove_origin_tags:
            tag_name = check_json_by_key(remove_local_tag, 'tag_name')
            if tag_name == '':
                log_printer('remove_tags_origin [ tag_name ] is "" so pass\n', "w", True)
            else:
                cmd_line = 'git push origin :refs/tags/%s' % tag_name
                remove_tag_res = exec_cli(cmd_line, local_p, out_of_time_default)
                if not remove_tag_res:
                    exit(1)


def merge_origin_branch(local_p, new_tag_js, branch_p):
    """
    合并远程分支，从 tag_git -> new -> merge_origin_branch 读取
    合并完成将回到 branch_p 入参的分支
    在 tag_git -> new -> push_origin 值为 1
    :param local_p: git 运行目录
    :param new_tag_js: tag_git -> new 转换的字典
    :param branch_p: 回切分支
    :return: 如果有操作，出错返回 False，其他情况为 True
    """
    if 'merge_origin_branch' in new_tag_js:
        branch_for_merge = new_tag_js['merge_origin_branch']
        cmd_git_checkout = 'git checkout %s' % branch_for_merge
        checkout_res = exec_cli(cmd_git_checkout, local_p, out_of_time_default)
        if not checkout_res:
            log_printer('merge origin checkout fail -> %s' % cmd_git_checkout, 'e', True)
            return False
        cmd_git_merge = 'git merge origin/%s' % branch_for_merge
        git_merge_res = exec_cli(cmd_git_merge, local_p, out_of_time_default)
        if not git_merge_res:
            log_printer('merge origin merge fail -> %s' % cmd_git_checkout, 'e', True)
            return False
        if 'push_origin' in new_tag_js.keys():
            push_origin = new_tag_js['push_origin']
            if 1 == push_origin:
                cmd_git_merge_push = 'git push -v origin/%s' % branch_for_merge
                git_merge_push_res = exec_cli(cmd_git_merge_push, local_p, out_of_time_default)
                if not git_merge_push_res:
                    log_printer('merge origin merge push fail -> %s' % cmd_git_checkout, 'e', True)
        cmd_git_checkout_from = 'git checkout %s' % branch_p
        git_checkout_from_res = exec_cli(cmd_git_checkout_from, local_p, out_of_time_default)
        if not git_checkout_from_res:
            log_printer('merge origin merge check out from fail -> %s' % cmd_git_checkout, 'e', True)
        return True
    else:
        log_printer('merge origin branch not set', 'i', False)
    return True


def new_git_tag(local_p, tag_git, branch_p):
    """
    这个函数，除了可以增加一个tag外，还会尝试合并远程分支
    :param local_p: 运行目录
    :param tag_git: tag json 字典
    :param branch_p: 父节点分支设置
    :return:
    """
    if 'new' in tag_git.keys():
        new_tag = check_json_by_key(tag_git, 'new')
        tag_name = check_json_by_key(new_tag, 'tag_name')
        if tag_name == '':
            log_printer('new tag name is "" so pass', "w", True)
        else:
            tag_message = check_json_by_key(new_tag, 'tag_message')
            git_add_and_commit_by_message(local_p, tag_message)
            cmd_git_add = 'git tag -a "%s" -m "%s"' % (tag_name, tag_message)
            add_res = exec_cli(cmd_git_add, local_p, out_of_time_default)
            if not add_res:
                log_printer('tag not add but can do to_next_version_tasks', 'w', True)
            if not merge_origin_branch(local_p, new_tag, branch_p):
                log_printer('merge origin branch fail', 'e', True)
                return
            if 'to_next_version_tasks' in new_tag.keys():
                to_next_version_tasks = check_json_by_key(new_tag, 'to_next_version_tasks')
                if len(to_next_version_tasks) > 0:
                    file_to = ''
                    for to_next_version_task in to_next_version_tasks:
                        task_name = check_json_by_key(to_next_version_task, 'name')
                        path_file = check_json_by_key(to_next_version_task, 'file')
                        file_from = check_json_by_key(to_next_version_task, 'from')
                        file_to = check_json_by_key(to_next_version_task, 'to')
                        abs_task_path = os.path.join(local_p, path_file)
                        if not check_dir_or_file_is_exist(abs_task_path):
                            log_printer('can not find to_next_version_tasks file at [ %s ]' % abs_task_path, 'e', True)
                        else:
                            log_printer(
                                'try to do to_next_version_tasks\n-> Name: -> %s\n-> File: %s\n-> from: %s\n-> to: %s' % (
                                    task_name, abs_task_path, file_from, file_to), 'i', True)
                            replace_text(abs_task_path, file_from, file_to)

                    git_add_and_commit_by_message(local_p, 'to new version for dev -> %s' % file_to)

            if not mode_test:
                if 'push_origin' in new_tag.keys():
                    push_origin = new_tag['push_origin']
                    if push_origin == 1:
                        if add_res:
                            cmd_git_tag_push = 'git push origin %s' % tag_name
                            push_res = exec_cli(cmd_git_tag_push, local_p, out_of_time_default)
                            if not push_res:
                                exit(1)

                        cmd_git_push = 'git push'
                        push_res = exec_cli(cmd_git_push, local_p, out_of_time_default)
                        if not push_res:
                            exit(1)


def filter_project_config(project, build_path=str):
    name_p = project['name']
    log_printer('\n=== start project %s ===\n' % name_p, 'i', True)
    git_url_p = check_json_by_key(project, 'git_url')
    local_p = check_json_by_key(project, 'local')
    local_p = os.path.join(build_path, local_p)
    branch_p = check_json_by_key(project, 'branch')
    tag_git = check_json_by_key(project, 'tag_git')
    if len(tag_git) < 1:
        log_printer('tag_git size less than 1 at %s exit!' % project, 'e', True)
        exit(1)
    auto_clean_p = check_json_by_key(project, 'auto_clean')
    clone_by_tag_or_not_has_tag(branch_p, git_url_p, local_p, project)
    version_check = check_version_file_when_has_version_check(local_p, project)
    if version_check:
        run_tag_file_tasks_if_has(local_p, project)
        new_git_tag(local_p, tag_git, branch_p)
        remove_tags_local(local_p, tag_git)
        remove_tags_origin(local_p, tag_git)
    if auto_clean_p != 0:
        auto_clean_build_project(local_p)
    log_printer('\n=== end project %s ===\n' % name_p, 'i', True)


def parser_tag_config_json(parser_json_path=str):
    """
    解析时，使用 "same_parser_params" 同样节点的参数
    如果 "parser_projects" 数组节点中，有个性参数，将覆盖共性参数
    :param parser_json_path:
    :return:
    """
    # type: str -> None
    global is_verbose
    parser_json_path = os.path.join(root_run_path, parser_json_path)
    if not os.path.exists(parser_json_path):
        log_printer("can not find json parser, exit!", 'e', True)
        exit(1)
    else:
        log_printer('Load parser path at: %s\n' % parser_json_path, 'i', True)
        try:
            with open(parser_json_path, 'r') as load_js:
                parser_js = json.load(load_js)
                parser_out_path = str(check_json_by_key(parser_js, 'parser_out_path'))
                if parser_out_path.startswith('./'):
                    true_path = parser_out_path[2:]
                    parser_out_path = os.path.join(root_run_path, true_path)
                if os.path.exists(parser_out_path):
                    log_printer('out parser path at: [ %s ] exists, exit by Error\n' % parser_out_path, 'e', True)
                    exit(1)
                else:
                    parser_build_path = str(check_json_by_key(parser_js, 'parser_build_path'))
                    parser_mode = str(check_json_by_key(parser_js, 'parser_mode'))
                    same_parser_params = check_json_by_key(parser_js, 'same_parser_params')
                    parser_projects = check_json_by_key(parser_js, 'parser_projects')
                    if len(parser_projects) < 1:
                        log_printer('parser_projects size less than 1 at %s exit!' % parser_projects, 'e', True)
                        exit(1)
                    build_project_list = []
                    for parser_project in parser_projects:
                        parser_project = dict(same_parser_params, **parser_project)
                        build_project_list.append(parser_project)
                    out_js = {
                        'build_path': parser_build_path,
                        'mode': parser_mode,
                        'build_projects': build_project_list
                    }
                    json_str = json.dumps(out_js, sort_keys=True, indent=2, separators=(',', ': '))
                    out_p_f = open(parser_out_path, 'w')
                    out_p_f.write(json_str)
                    out_p_f.close()
        except Exception, e:
            log_printer('Read json config file: %s\n%s\nError, exit!' % (parser_json_path, str(e)), 'e', True)
            exit(1)
    pass


def parser_clean_and_try_clean(c_clean=str):
    global config_file_path
    check_clean_path = os.path.join(root_run_path, c_clean)
    if os.path.exists(check_clean_path):
        config_file_path = check_clean_path
    if os.path.exists(config_file_path):
        js = read_json_file(config_file_path)
        build_path = js['build_path']
        build_path = os.path.join(root_run_path, build_path)
        change_files_write(build_path)
        time.sleep(1)
        shutil.rmtree(build_path, True)
        time.sleep(1)
        log_printer('Clean success : %s' % build_path, 'i', True)
    else:
        log_printer('can not find path %s\nExit 1!' % config_file_path, 'e', True)
        exit(1)


if __name__ == '__main__':
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
    parser.add_option('-f', '--force', dest='f_force', action="store_true",
                      help="force run not set check", default=False)
    parser.add_option('--test', dest='c_test', action="store_true",
                      help="set mode of test", default=False)
    parser.add_option('--clean', dest='c_clean', type="string",
                      help="clean you set if not set use run path tag.json"
                      , metavar="tag.json")
    parser.add_option('--config', dest='c_config', type="string",
                      help="build config json file if not set use run path tag.json"
                      , metavar="tag.json")
    parser.add_option('--parser', dest='c_parser', type="string",
                      help="parser config.json file by config"
                      , metavar="tag_parser.json")
    (options, args) = parser.parse_args()
    logger = init_logger_by_time(this_tag)
    if options.v_verbose:
        is_verbose = True
    config_file_path = os.path.join(root_run_path, 'tag.json')
    if options.f_force:
        is_force = True
    if options.c_test:
        mode_test = True
    if options.c_clean:
        parser_clean_and_try_clean(options.c_clean)
        exit(0)
    elif options.c_config:
        read_json_config(options.c_config)
        exit(0)
    elif options.c_parser:
        parser_tag_config_json(options.c_parser)
        exit(0)
