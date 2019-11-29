#!/usr/bin/env python
# -*- coding: utf-8 -*-
import optparse
import os
import platform
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    # print('change encoding error {}'.format(e))
    pass

folder_path = os.getcwd()


class PLog:
    def __init__(self):
        pass

    _runtime_version_error = """
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

    _is_verbose = False

    @staticmethod
    def _is_sys_windows():
        return platform.system() == "Windows"

    @staticmethod
    def set_verbose(verbose=False):
        PLog._is_verbose = verbose

    @staticmethod
    def check_runtime():
        PLog.log('Python version %s' % platform.python_version(), 'd')
        version_split = platform.python_version().split('.')
        if version_split[0] != '2':
            PLog.log(PLog._runtime_version_error, 'e', True)
            exit(1)
        if version_split[1] < '6':
            PLog.log(PLog._runtime_version_error, 'e', True)
            exit(1)

    @staticmethod
    def log_normal(info):
        if not PLog._is_sys_windows():
            print (PLog.WRITE + info + PLog.END_LI)
        else:
            print (info)

    @staticmethod
    def log_assert(info):
        if not PLog._is_sys_windows():
            print (PLog.BLACK + info + PLog.END_LI)
        else:
            print (info)

    @staticmethod
    def log_info(info):
        if not PLog._is_sys_windows():
            print (PLog.OK_GREEN + info + PLog.END_LI)
        else:
            print (info)

    @staticmethod
    def log_debug(info):
        if not PLog._is_sys_windows():
            print (PLog.OK_BLUE + info + PLog.END_LI)
        else:
            print (info)

    @staticmethod
    def log_warning(info):
        if not PLog._is_sys_windows():
            print (PLog.WARNING + info + PLog.END_LI)
        else:
            print (info)

    @staticmethod
    def log_error(info):
        if not PLog._is_sys_windows():
            print (PLog.ERROR + info + PLog.END_LI)
        else:
            print (info)

    @staticmethod
    def log(msg, lev=str, must=False):
        # type: (str, str, bool) -> None
        if not PLog._is_sys_windows():
            if lev == 'i':
                if PLog._is_verbose or must:
                    PLog.log_info('%s' % msg)
            elif lev == 'd':
                if PLog._is_verbose or must:
                    PLog.log_debug('%s' % msg)
            elif lev == 'w':
                PLog.log_warning('%s' % msg)
            elif lev == 'e':
                PLog.log_error('%s' % msg)
            elif lev == 'a':
                PLog.log_assert('%s' % msg)
            else:
                if PLog._is_verbose or must:
                    PLog.log_normal('%s' % msg)
        else:
            if lev == 'w' or lev == 'e':
                print('%s\n' % msg)
            else:
                if PLog._is_verbose or must:
                    print('%s\n' % msg)


class OptDefClass:
    hint_help_info = """
must use faker by pip install XXX
more information see script code.
"""

    cwd_script_file_name = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:]
    enter_error_info = """
    Your input error
        Usage:
            python {0} --help
    or input:
        ./{0} -h to see help
    """.format(cwd_script_file_name)

    msg_open_force_mode = r'! warning open force mode'
    msg_interrupt_generate = r'generate interrupt, if you want to continue use --force'

    def __init__(self):
        self.options = None
        self.args = None
        self_parser = optparse.OptionParser('\n\t%prog' + ' -h\n\t%prog -v -c\n' + OptDefClass.hint_help_info)
        self_parser.add_option('-v', dest='v_verbose', action="store_true",
                               help="see verbose",
                               default=False)
        self_parser.add_option('--force', dest='force', action="store_true",
                               help="do job force, ignore warning",
                               default=False)
        self_parser.add_option('-f', '--targetFile', dest='f_targetFile', type="string",
                               help="target file default is README.md",
                               default="README.md",
                               metavar="README.md")
        self_parser.add_option('-c', '--clean', dest='c_clean', action="store_true",
                               help="clean after cli",
                               default=False)
        self.options, self.args = self_parser.parse_args()

    def opt(self):
        return self.options

    def args(self):
        return self.args

    def verification(self):
        if not self.options.f_targetFile or not self.options.c_clean:
            exit('ERROR!must support --clean and --targetFile parameters!')


if __name__ == '__main__':
    PLog.check_runtime()
    if len(sys.argv) < 2:
        PLog.log(OptDefClass.enter_error_info, 'e', True)
        exit(1)

    opt = OptDefClass()
    opt.verification()

    options = opt.opt()
    # --verbose
    if options.v_verbose:
        PLog.set_verbose(options.v_verbose)

    # --force
    if options.force:
        PLog.log(OptDefClass.msg_open_force_mode, 'w')

    # --clean
    if options.c_clean:
        PLog.log('now clean flag {0} force flag {1}'.format(options.c_clean, options.force), 'd')
