#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jenkins

import os
import sys
import platform
import stat
import time
import datetime
import inspect
import logging
import logging.handlers
import getpass

import optparse

__author__ = 'sinlov'

reload(sys)
sys.setdefaultencoding('utf-8')

user_id = 'userID'
api_token = 'userToken'

jenkins_server_url = 'http://xx.com/jenkins/'
jenkins_replace_url = 'http://xx.com/jenkins/'

"""
自动清空日志的时间差，为三周
"""
out_of_time_log_auto_clean = 60 * 60 * 24 * 7 * 3
"""
日志标记
"""
this_tag = 'log_ci_xx_jenkins_'
"""
默认日志目录
"""
log_folder = 'log_xx_jenkins'


is_verbose = False
root_run_path = os.getcwd()

class Logger_Print:
    def __init__(self):
        pass

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
                Logger_Print.log_normal('%s' % msg)
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


def time_stamp_mark():
    """
    Time mark %y.%m.%d.%M.%S
    :return: time string
    """
    now = datetime.datetime.now()
    return now.strftime('%y.%m.%d.%M.%S')


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
        log_printer('delete path error %s' % str(e), 'e', True)


def call_jenkins_base_info():
    version = server.get_version()
    log_printer('Jenkins Info =>\nJenkins version -> %s' % version, 'a', True)
    if is_verbose:
        who_am_i = server.get_whoami()
        log_printer('Jenkins whoami -> %s' % who_am_i['fullName'], 'i', True)
        if 'id' in who_am_i:
            log_printer('Jenkins id -> %s' % who_am_i['id'], 'i', True)
        if 'absoluteUrl' in who_am_i:
            absolute_url = who_am_i['absoluteUrl']
            absolute_url_replace = absolute_url.replace(jenkins_replace_url, jenkins_server_url)
            log_printer('Jenkins absoluteUrl -> %s' % absolute_url_replace, 'i', True)
        if 'address' in who_am_i:
            log_printer('Jenkins email-address -> %s' % who_am_i['address'], 'i', True)
        if 'address' in who_am_i:
            log_printer('Jenkins email-address -> %s' % who_am_i['address'], 'i', True)
        if 'property' in who_am_i:
            property_list = who_am_i['property']
            for property in property_list:
                if 'insensitiveSearch' in property:
                    log_printer('Jenkins insensitiveSearch status -> %s' % property['insensitiveSearch'], 'i', True)
        jobs_count = server.jobs_count()
        log_printer('Jenkins job count -> %s' % jobs_count, 'i', True)
    pass


def call_jenkins_job_build_by_full_name(full_job_name=str, last_status=str, force=False):
    # type: (str, str, bool) -> None
    job_exists = server.job_exists(full_job_name)
    if job_exists:
        status = call_jenkins_job_last_status(full_job_name)
        if status == 'ANY' or force:
            call_jenkins_build_by_name(full_job_name)
            log_printer('-> jenkins call status: ANY\nBuild name: %s' % full_job_name, 'i', True)
        else:
            if status == last_status:
                is_not_building = is_not_jenkins_job_in_building(full_job_name)
                if is_not_building or force:
                    call_jenkins_build_by_name(full_job_name)
                    log_printer('-> jenkins call status: %s\nBuild name: %s' % (status, full_job_name), 'i',
                                True)
                else:
                    log_printer('-> jenkins job is building \nBuild name: %s' % full_job_name,
                                'w', True)
            else:
                log_printer(
                    '-> cancel call jenkins build %s last_status [ %s ]' % (full_job_name, str(status)),
                    'w', True)
    else:
        log_printer('-> job is not exist: %s' % full_job_name, 'e', True)
    pass


def call_jenkins_job_build_by_filter(job_filter, last_status, force=False):
    jobs = server.get_all_jobs()
    log_printer('=> jenkins build filter: %s' % str(job_filter), 'a', True)
    call_count = 0
    for job in jobs:
        if 'fullname' in job:
            full_name_find = job['fullname']
            if job_filter in full_name_find:
                log_printer('\n-> build jenkins info start <-', 'i', True)
                if 'name' in job:
                    log_printer('-> jenkins name: %s' % str(job['name']), 'i', True)
                if 'color' in job:
                    log_printer('-> jenkins color: %s' % str(job['color']), 'i', True)
                if 'url' in job:
                    find_url = str(job['url'])
                    find_url_replace = find_url.replace(jenkins_replace_url, jenkins_server_url)
                    log_printer('-> jenkins url: %s' % find_url_replace, 'i', True)
                status = call_jenkins_job_last_status(full_name_find)
                if status == 'ANY' or force:
                    call_jenkins_build_by_name(full_name_find)
                    log_printer('-> jenkins call status: ANY\nBuild name: %s' % full_name_find, 'i', True)
                    call_count += 1
                else:
                    if status == last_status:
                        is_not_building = is_not_jenkins_job_in_building(full_name_find)
                        if is_not_building or force:
                            call_jenkins_build_by_name(full_name_find)
                            log_printer('-> jenkins call status: %s\nBuild name: %s' % (status, full_name_find), 'i',
                                        True)
                            call_count += 1
                        else:
                            log_printer('-> jenkins job is building \nBuild name: %s' % full_name_find,
                                        'w', True)
                    else:
                        log_printer(
                            '-> cancel call jenkins build %s last_status [ %s ]' % (full_name_find, str(status)),
                            'w', True)
                log_printer('-> build jenkins info end <-\n', 'i', True)
    log_printer('=> full jenkins call count %s' % call_count, 'a', True)
    pass


def is_job_exist(job_full_name):
    return server.job_exists(job_full_name)


def call_jenkins_build_by_name(build_url):
    server.build_job(build_url)
    log_printer('build_url [ %s ]' % build_url, 'd')
    pass


def is_not_jenkins_job_in_building(job_full_name):
    build_last_check = server.get_job_info(job_full_name)['lastBuild']
    if build_last_check:
        number_last = build_last_check['number']
        building_mark = server.get_build_info(job_full_name, number_last)['building']
        log_printer('building_mark [ %s ]' % building_mark, 'd')
        return not building_mark
    return True


def call_jenkins_job_last_status(job_full_name):
    info = server.get_job_info(job_full_name)
    if 'lastBuild' in info:
        build_last = info['lastBuild']
        if build_last:
            if 'number' in build_last:
                number_last = build_last['number']
                log_printer('number_last [ %s ]' % str(number_last), 'd')
                return server.get_build_info(job_full_name, number_last)['result']
            else:
                return False
        else:
            return False
    else:
        return False


def call_jenkins_search(job_name=str):
    jobs = server.get_all_jobs()
    job_name_lower = job_name.lower()
    log_printer('job_name [ %s ]' % job_name_lower, 'd')
    search_count = 0
    for job in jobs:
        if 'fullname' in job:
            full_name_find = job['fullname']
            if job_name_lower in str(full_name_find).lower():
                log_printer('-> jenkins build job full name: [ %s ]' % str(full_name_find), 'i', True)
                if 'name' in job:
                    log_printer('-> jenkins name: %s' % str(job['name']), '', True)
                if 'color' in job:
                    log_printer('-> jenkins color: %s' % str(job['color']), 'i', True)
                if 'url' in job:
                    find_url = str(job['url'])
                    find_url_replace = find_url.replace(jenkins_replace_url, jenkins_server_url)
                    log_printer('-> jenkins url: %s' % find_url_replace, '', True)
                    log_printer(
                        '-> jenkins lastBuild URL: %slastSuccessfulBuild/artifact/*zip*/archive.zip' % find_url_replace,
                        '', True)
                    log_printer(
                        '-> jenkins BuildDownload URL: %s[build_number]/artifact/*zip*/archive.zip' % find_url_replace,
                        '', True)
                status = call_jenkins_job_last_status(full_name_find)
                if status == 'SUCCESS':
                    log_printer('-> jenkins last status: %s' % status, 'i', True)
                else:
                    log_printer('-> jenkins last status: %s' % status, 'w', True)
                not_building = is_not_jenkins_job_in_building(full_name_find)
                log_printer('-> jenkins is building: %s' % str(not not_building), 'd', True)
                search_count += 1
    log_printer('=> full search count: %s' % str(search_count), 'a', True)


def cancel_full_jenkins_build():
    running_builds = server.get_running_builds()
    jobs = server.get_all_jobs()
    cancel_count = 0
    for build in running_builds:
        build_number = 0
        build_url = ''
        if 'name' in build:
            name_find = build['name']
            log_printer('-> running build name: %s' % str(name_find), 'i', True)
        if 'node' in build:
            log_printer('-> running build node: %s' % str(build['node']), 'i', True)
        if 'url' in build:
            build_url = str(build['url'])
            find_url_replace = build_url.replace(jenkins_replace_url, jenkins_server_url)
            log_printer('-> running build url: %s' % find_url_replace, 'i', True)
        if 'number' in build:
            build_number = build['number']
        for job in jobs:
            if 'url' in job:
                find_url = str(job['url'])
                if find_url == build_url.replace('%s/' % build_number, ''):
                    full_name_find = job['fullname']
                    server.stop_build(full_name_find, build_number)
                    log_printer('-> stop build fullname: %s' % full_name_find, 'i', True)
                    log_printer('-> stop build build_number: %s' % build_number, 'i', True)
                    cancel_count += 1
        log_printer('=> full cancel build count: %s' % cancel_count, 'a', True)
    pass


def cancel_jenkins_build_by_full_name(cancel_full_name):
    job_exists = server.job_exists(cancel_full_name)
    if job_exists:
        running_builds = server.get_running_builds()
        cancel_count = 0
        build_number = 0
        for build in running_builds:
            if 'number' in build:
                build_number = build['number']
            if 'name' in build:
                name_find = build['name']
                if name_find in cancel_full_name:
                    log_printer('-> cancel build name: %s' % cancel_full_name, 'd')
                    if 'url' in build:
                        build_url = str(build['url'])
                        find_url_replace = build_url.replace(jenkins_replace_url, jenkins_server_url)
                        log_printer('-> running build url: %s' % find_url_replace, 'i', True)
                    server.stop_build(cancel_full_name, build_number)
                    log_printer('-> stop build fullname: %s' % cancel_full_name, 'i', True)
                    log_printer('-> stop build build_number: %s' % build_number, 'i', True)
                    cancel_count += 1
        if cancel_count == 0:
            log_printer('-> job is not building: %s' % cancel_full_name, 'e', True)
    else:
        log_printer('-> job is not exist: %s' % cancel_full_name, 'e', True)
    pass


def call_jenkins_email_notification(job_name, job_status, force):
    job_exists = server.job_exists(job_name)
    if not job_exists:
        log_printer('-> job is not exist: %s' % job_name, 'e', True)
    else:
        log_printer('-> wait for dev %s' % job_name, 'i', True)
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must input params or see -h"
        exit(1)
    check_p = str(sys.argv[1])
    if not check_p.startswith('-'):
        print 'You params is error please see -h'
        exit(1)
    parser = optparse.OptionParser(
        '%prog' + '\n\tThis utils must use before run [ pip install python-jenkins ]'
                  '\n\tTest jenkins connect\t%prog --info'
                  '\n\tJenkins search job\t%prog -s jobName [upper case as same]'
                  '\n\tJenkins build job\t%prog -b -j jobNameFullName [must use job full name]'
                  '\n\tMore info see http://python-jenkins.readthedocs.io/en/latest/api.html'
    )
    # config api
    parser.add_option('--verbose', dest='v_verbose', action="store_true",
                      help="see verbose", default=False)
    parser.add_option('-f', '--force', dest='f_force', action="store_true",
                      help="is force do job", default=False)
    # server api
    parser.add_option('--info', dest='server_info', action="store_true",
                      help="see jenkins server info", default=False)
    parser.add_option('-u', '--user', dest='u_user', type="string",
                      help="jenkins user_id", metavar="userID")
    parser.add_option('--api_token', dest='a_api_token', type="string",
                      help="jenkins api_token", metavar="token")
    parser.add_option('--server', dest='j_server', type="string",
                      help="jenkins server url", metavar=jenkins_server_url)
    parser.add_option('--server_hint', dest='j_server_hint', type="string",
                      help="jenkins server url for replace show of address", metavar=jenkins_replace_url)
    parser.add_option('-s', '--search', dest='s_search', type="string",
                      help="search job by name", metavar='job')
    # job api
    parser.add_option('-j', dest='job_full_name', type="string",
                      help="jenkins job full name", metavar="Job/job-name")
    parser.add_option('--status', dest='status', type="string",
                      help="call build jenkins filter status", metavar='[ ANY SUCCESS ABORTED None FAILURE ]')
    # biz api
    parser.add_option('-b', '--buildOne', dest='build_one', action="store_true",
                      help="jenkins build one job by full name", default=False)
    parser.add_option('--cancelOne', dest='cancel_one', type="string",
                      help="jenkins cancel one job by full name", metavar="Job/job-name")
    parser.add_option('--cancelAll', dest='cancel_all', action="store_true",
                      help="cancel all build job", default=False)
    parser.add_option('--filterBuild', dest='build_filter', type="string",
                      help="call build jenkins filter", metavar="job")
    parser.add_option('--email-notification', dest='email_notification', type="string",
                      help="jenkins change email-notification ", metavar="Job/job-name")

    (options, args) = parser.parse_args()
    logger = init_logger_by_time(this_tag)
    if options.v_verbose:
        is_verbose = True
    # config_file_path = os.path.join(root_run_path, "jenkins.json")
    # if options.config:
    #     config_file_path = options.config
    # log_printer('Load config path at: %s\n' % config_file_path, 'i', True)
    if options.u_user:
        user_id = options.u_user
    if options.a_api_token:
        api_token = options.a_api_token
    if options.j_server:
        jenkins_server_url = options.j_server
    if options.j_server_hint:
        jenkins_replace_url = options.j_server_hint
    job_full_name = ""
    job_status = 'SUCCESS'
    try:
        if options.job_full_name:
            job_full_name = options.job_full_name
        if options.status:
            job_status = options.status
        log_printer('Try to connect jenkins server: %s' % jenkins_server_url, 'i', True)
        server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)
        if options.server_info:
            is_verbose = True
            call_jenkins_base_info()
            exit(0)
        elif options.s_search:
            log_printer('=> jenkins job search...', 'a', True)
            call_jenkins_search(options.s_search)
            exit(0)
        elif options.build_one:
            if job_full_name == '':
                log_printer('Error call jenkins buildOne because or [ -j ] not set!', 'e', True)
                exit(1)
            else:
                call_jenkins_job_build_by_full_name(job_full_name, job_status, options.f_force)
                exit(0)
        elif options.cancel_one:
            cancel_jenkins_build_by_full_name(options.cancel_one)
            exit(0)
        elif options.cancel_all:
            cancel_full_jenkins_build()
            exit(0)
        elif options.build_filter:
            call_jenkins_job_build_by_filter(options.build_filter, job_status, options.f_force)
        elif options.email_notification:
            if job_full_name == '':
                log_printer('Error call jenkins --email-notification because or [ -j ] not set!', 'e', True)
                exit(1)
            else:
                call_jenkins_email_notification(job_full_name, job_status, options.f_force)
                exit(0)
        else:
            call_jenkins_base_info()
            exit(0)
    except Exception as e:
        log_printer('Error call server: %s\nError Info: %s\nOr not run [ pip install python-jenkins ]\nExit!' % (
            jenkins_server_url, str(e)), 'e', True)
        exit(1)
