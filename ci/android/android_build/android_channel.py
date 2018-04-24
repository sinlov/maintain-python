#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import platform
import optparse
import zipfile

__author__ = 'sinlov'

is_verbose = False
folder_path = os.getcwd()
resource_file = ""
out_file = ""
channel_name = ""
properties_file = ""

hint_help_info = """
more information see below
"""

enter_error_info = """
Your input error
    Usage:
        ./temp.py --help
    or input [-h] to see help
"""

runtime_version_error = """
This script must run python 2.6.+
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
    def check_runtime():
        PLog.log('Python version %s' % platform.python_version(), 'd')
        version_split = platform.python_version().split('.')
        if version_split[0] != '2':
            PLog.log(runtime_version_error, 'e', True)
            exit(1)
        if version_split[1] < '6':
            PLog.log(runtime_version_error, 'e', True)
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


def inject_apk_channel_file(resource=str, channel_name_def=str, properties=str):
    try:
        PLog.log('from file [{0}]'.format(resource), 'i', is_verbose)
        zipped = zipfile.ZipFile(resource, 'a', zipfile.ZIP_DEFLATED)
        channel_file_name = "META-INF/pl_channel_{channel_name}".format(channel_name=channel_name_def)
        PLog.log('inject channel file [{0}]'.format(channel_file_name), 'i', is_verbose)
        zipped.write(properties, channel_file_name)
        zipped.close()
        PLog.log('inject apk as channel [{0}] to path [{1}]\nSuccess'.format(channel_name_def, resource))
    except Exception as e:
        PLog.log('inject_apk_channel_file %s' % str(e), 'e', True)
        pass


if __name__ == '__main__':
    PLog.check_runtime()
    folder_path = ''
    if len(sys.argv) < 2:
        PLog.log(enter_error_info, 'e', True)
        exit(1)
    parser = optparse.OptionParser('\n\t%prog' + ' -h\n\t%prog -v -c\n' + hint_help_info)
    parser.add_option('-v', dest='v_verbose', action="store_true", help="see verbose", default=False)
    parser.add_option('-r', '--resource', dest='r_resource', type="string", help="path of resource apk is .",
                      default="", metavar="res.apk")
    parser.add_option('-o', '--out', dest='o_out', type="string", help="path of out apk is .",
                      default="", metavar="out.apk")
    parser.add_option('-c', '--channel', dest='c_channel', type="string", help="channel .",
                      default="", metavar="base")
    parser.add_option('-p', '--properties', dest='p_properties', type="string", help="properties file .",
                      default="", metavar="osCiTest.properties")
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    if options.r_resource:
        resource_file = options.r_resource
        if not os.path.exists(resource_file):
            PLog.log('can not found resource file as [%s]' % resource_file, 'e', True)
            exit(1)
    if options.o_out:
        out_file = options.o_out
        if os.path.exists(out_file):
            PLog.log('out file is exists as [%s]' % out_file, 'e', True)
            exit(1)
    if options.c_channel:
        channel_name = options.c_channel
    if options.p_properties:
        properties_file = options.p_properties
        if not os.path.exists(properties_file):
            PLog.log('can not found properties file as [%s]' % properties_file, 'e', True)
            exit(1)

    if channel_name == "":
        PLog.log('channel name is empty', 'e', True)
        exit(1)
    shutil.copyfile(resource_file, out_file)
    inject_apk_channel_file(out_file, channel_name, properties_file)
