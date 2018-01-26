#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import platform
import optparse

__author__ = 'sinlov'

is_verbose = False
top_level = 1
folder_path = os.getcwd()

hint_help_info = """
more information see
"""

enter_error_info = """
Your input error
    Usage:
        ./as_gradle_update_2_to_3.py --help
    or input [-h] to see help
"""


class PLog:
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
                print '%s\n' % msg


def is_platform_windows():
    sys_str = platform.system()
    if sys_str == "Windows":
        return True
    else:
        return False


def find_out_base():
    pass


def update_as_project_2_to_3(update_path):
    if not os.path.exists(update_path):
        PLog.log("Error your input Folder %s is not exist" % update_path, 'e', True)
        exit(1)
    if os.path.isdir(update_path) < 1:
        PLog.log("Error your input path %s is not folder" % update_path, 'e', True)
        exit(1)
    modules = check_settings_gradle(update_path)
    if len(modules) == 0:
        PLog.log("Error your input path %s not found settings.gradle" % update_path, 'e', True)
        exit(1)
    else:
        PLog.log('module is %s' % modules, "i", True)


def check_settings_gradle(update_path):
    dev_modules = []
    settings_gradle_path = os.path.join(update_path, 'settings.gradle')
    if not os.path.exists(settings_gradle_path):
        return dev_modules
    else:
        try:
            settings_lines = open(settings_gradle_path, 'r').readlines()
            for line in range(len(settings_lines) - 1):
                if str(line).startswith('include'):
                    # line.
                    dev_modules.append(line)
        except Exception, e:
            PLog.log("check_settings_gradle error, error info %s" % str(e), 'e', True)
            dev_modules = []
        return dev_modules


if __name__ == '__main__':
    folder_path = ''
    if len(sys.argv) < 2:
        PLog.log(enter_error_info, 'e', True)
        exit(1)
    parser = optparse.OptionParser('\n%prog ' + ' -p \n\tOr %prog <folder>\n' + hint_help_info)
    parser.add_option('-v', dest='v_verbose', action="store_true", help="see verbose", default=False)
    parser.add_option('-f', '--folder', dest='f_folder', type="string", help="path of folder Default is .",
                      default=".", metavar=".")
    parser.add_option('-l', '--level', dest='l_level', type="int", help="top level Default 7",
                      default=7, metavar=7)
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    if options.l_level is not None:
        top_level = options.l_level
    if options.f_folder is not None:
        folder_path = options.f_folder
        update_as_project_2_to_3(folder_path)
