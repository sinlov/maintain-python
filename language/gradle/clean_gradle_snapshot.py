#!/usr/bin/env python

# coding=utf-8

import os
import sys
import platform
import stat
import time
import inspect

import shutil

import logging
import logging.handlers
import getpass

import optparse

__author__ = 'sinlov'

reload(sys)
sys.setdefaultencoding('utf-8')

is_verbose = False
root_run_path = os.getcwd()

this_tag = 'clean_'
log_time_format = '%Y_%m_%d_%H_%M_%S'

"""
auto clean time default is one week
"""
out_of_time_log_auto_clean = 60 * 60 * 24 * 7

gradle_snapshot_mark = '-SNAPSHOT'
gradle_file_2_1_path = os.path.join(os.path.expandvars('$HOME'), '.gradle', 'caches', 'modules-2', 'files-2.1')


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


def check_current_log_path_and_auto_clean():
    """
    auto clean log by :out_of_time_log_auto_clean
    :return:
    """
    log_path = os.path.join(current_file_directory(), 'log')
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


def find_now_time_format(format_time):
    # type: (str) -> format_time
    """
    :return: time string
    """
    return time.strftime(format_time, time.localtime(time.time()))


def init_logger_by_time(tag=str):
    # type: (str) -> tag
    return init_logger(tag, find_now_time_format(log_time_format))


def log_printer(msg, lev=str, must=False):
    # type: (str, str, bool) -> None
    if is_verbose or must:
        print msg,
    if lev == 'i':
        logger.info(msg)
    elif lev == 'd':
        logger.debug(msg)
    elif lev == 'w':
        logger.warning(msg)
    elif lev == 'e':
        logger.error(msg)
    else:
        logger.info(msg)


def is_platform_windows():
    sys_str = platform.system()
    if sys_str == "Windows":
        return True
    else:
        return False


def current_file_directory():
    path = os.path.realpath(sys.path[0])  # interpreter starter's path
    if os.path.isfile(path):  # starter is excutable file
        path = os.path.dirname(path)
        return os.path.abspath(path)  # return excutable file's directory
    else:  # starter is python script
        caller_file = inspect.stack()[1][1]  # function caller's filename
        return os.path.abspath(os.path.dirname(caller_file))  # return function caller's file's directory


def check_dir_or_file_is_exist(abs_path=str):
    return os.path.exists(abs_path)


def change_files_write(path=str):
    # type: (str) -> None
    for root, dirs, files in os.walk(path):
        for name in files:
            os.chmod(os.path.join(root, name), stat.S_IWRITE)
    logger.info('change change_files_write success')


def del_dot_head_files(dot_path=str):
    try:
        for root, dirs, files in os.walk(dot_path):
            for name in files:
                if name.startswith("."):
                    os.remove(os.path.join(root, name))
        logger.info("delete path " + dot_path + " success!")
    except Exception, e:
        logger.error(e)
        print e


def sorted_dict_values_to_list(s_dict):
    keys = s_dict.keys()
    keys.sort()
    return [s_dict[key] for key in keys]


def check_user_gradle_path():
    log_printer('try to find this user gradle file 2.1 path %s\n' % gradle_file_2_1_path, 'i', True)
    return check_dir_or_file_is_exist(gradle_file_2_1_path)


def clean_useless_gradle_catch_snapshot():
    """
    find default gradle catch name has gradle_snapshot_mark, remove others except last last modification
    :return:
    """
    if check_user_gradle_path():
        snapshot_path_list = find_out_snapshot_path_list()
        for snapshot_path in snapshot_path_list:
            for walk_dir, walk_folder, walk_file in os.walk(snapshot_path):
                now_folder = {}
                for d in walk_folder:
                    snapshot_hash_path = os.path.join(walk_dir, d)
                    m_time = os.path.getmtime(snapshot_hash_path)
                    now_folder[m_time] = snapshot_hash_path
                if len(now_folder) > 0:
                    new_sort = sorted_dict_values_to_list(now_folder)
                    for path in new_sort[0: -1]:
                        shutil.rmtree(path)
                        log_printer('remove useless snapshot at path\n-> %s' % path, 'i', True)
    else:
        log_printer('can not found gradle catch folder exit', 'e', True)
        exit(1)


def find_out_snapshot_path_list():
    """
    find out full folder which end with gradle_snapshot_mark which in gradle_file_2_1_path
    :return: path list
    """
    snapshot_path_arr = []
    for walk_dir, walk_folder, walk_file in os.walk(gradle_file_2_1_path):
        for d in walk_folder:
            if d.endswith(gradle_snapshot_mark):
                snapshot_path = os.path.join(walk_dir, d)
                snapshot_path_arr.append(snapshot_path)
    return snapshot_path_arr


def clean_old_gradle_catch_snapshot():
    print 'this way is developing! exit 0'
    pass


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
    parser.add_option('-c', '--cleanOld', dest='c_cleanOld', action="store_true",
                      help="clean you set build_path ", default=False)
    parser.add_option('-u', '--uselessClean', dest='u_uselessClean', action="store_true",
                      help="clean you set build_path last modification", default=False)
    parser.add_option('-f', '--force', dest='f_force', action="store_true",
                      help="force build not set check", default=False)
    (options, args) = parser.parse_args()
    logger = init_logger_by_time(this_tag)
    if options.v_verbose:
        is_verbose = True
    if options.u_uselessClean:
        try:
            clean_useless_gradle_catch_snapshot()
        except Exception, e:
            log_printer('just some error, please check %s' % str(e))
    if options.c_cleanOld:
        clean_old_gradle_catch_snapshot()

