#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import optparse

import re
import shutil
import time

__author__ = 'sinlov'

is_verbose = False
is_force = False
level_set = 1
folder_path = os.getcwd()

hint_help_info = """
more information see
"""

enter_error_info = """
Your input error
    Usage:
        ./jetbrain_index_clean.py --help
    or input [-h] to see help
"""

jetbrain_tools_list = [
    'AndroidStudio',
    'CLion',
    'DataGrip',
    'GoLand',
    'IntelliJIdea',
    'PhpStorm',
    'PyCharm',
    'RubyMine',
    'WebStorm'
]

clean_type_list = [
    'cleanCatchIndex',
    'cleanCatchAll'
]


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
        print (PLog.WRITE + info + PLog.END_LI)

    @staticmethod
    def log_assert(info):
        print (PLog.BLACK + info + PLog.END_LI)

    @staticmethod
    def log_info(info):
        print (PLog.OK_GREEN + info + PLog.END_LI)

    @staticmethod
    def log_debug(info):
        print (PLog.OK_BLUE + info + PLog.END_LI)

    @staticmethod
    def log_warning(info):
        print (PLog.WARNING + info + PLog.END_LI)

    @staticmethod
    def log_error(info):
        print (PLog.ERROR + info + PLog.END_LI)

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


def checkToolsByList(tools_name=str):
    if tools_name in jetbrain_tools_list:
        return True
    else:
        PLog.log('tools must in %s ' % jetbrain_tools_list, 'e', True)
        return False


def checkType(type_name=str):
    if type_name in clean_type_list:
        return True
    else:
        PLog.log('type must in %s ' % clean_type_list, 'e', True)
        return False


def find_jetbrain_catch_and_clean_index(tools_name=str, release_version=str):
    pass


def clean_jetbrain_by_type(type_name=str, tools_name=str, release_version=str):
    if type_name == 'cleanCatchIndex':
        find_jetbrain_catch_and_clean_index(tools_name, release_version)
    elif tools_name == 'cleanCatchAll':
        PLog.log('type %s now is develop can not use' % type_name, 'D', True)
    else:
        PLog.log('unsupport type %s' % type_name, 'e', True)
        exit(1)


if __name__ == '__main__':
    PLog.check_runtime()
    folder_path = ''
    if len(sys.argv) < 2:
        PLog.log(enter_error_info, 'e', True)
        exit(1)
    parser = optparse.OptionParser('\n%prog ' + ' -t AndroidStudio \n\t now only support macOS\n' + hint_help_info)
    parser.add_option('-v', dest='v_verbose', action="store_true", help="see verbose", default=False)
    parser.add_option('-t', '--tools', dest='t_tools', type="string",
                      help="want clean tools name, name error will out which support",
                      default="IntelliJIdea", metavar="IntelliJIdea")
    # parser.add_option('-l', '--level', dest='l_level', type="int", help="top level Default 7 now no use",
    #                   default=7, metavar=7)
    parser.add_option('-r', '--release', dest='r_release', type="string",
                      help="tools release version, if not find catch, will error",
                      default="", metavar="")
    parser.add_option('--type', dest='t_type', type="string", help="clean type, if not support will error",
                      default="cleanCatchIndex", metavar="cleanCatchIndex")
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    if options.t_tools:
        if not checkToolsByList(options.t_tools):
            exit(1)
    if options.t_type:
        if not checkType(options.t_type):
            exit(1)
    PLog.log('=> Jetbrain Info tool [ {0} ], release [ {2} ], cleanType [ {1} ]'.format(options.t_tools, options.t_type,
                                                                                        options.r_release), 'i', True)
    clean_jetbrain_by_type(options.t_type, options.t_tools, options.r_release)
