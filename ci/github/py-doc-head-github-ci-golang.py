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

ci_head_content = r"""
[![TravisBuildStatus](https://api.travis-ci.org/%s.svg?branch=master)](https://travis-ci.org/%s)
[![GoDoc](https://godoc.org/github.com/%s?status.png)](https://godoc.org/github.com/%s/)
[![GoReportCard](https://goreportcard.com/badge/github.com/%s)](https://goreportcard.com/report/github.com/%s)
[![codecov](https://codecov.io/gh/%s/branch/master/graph/badge.svg)](https://codecov.io/gh/%s)
"""


# folder_path = os.getcwd()


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


class DocHeadGithubCiGolang:
    hint_help_info = """
    must use faker by pip install XXX
    more information see
    """

    cwd_script_file_name = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:]
    enter_error_info = """
    Your input error
        Usage:
            python {0} --help
    or input:
        ./{0} -h to see help
    """.format(cwd_script_file_name)

    def __init__(self):
        self.options = None
        self.args = None
        self_parser = optparse.OptionParser(
            '\n\t%prog' + ' -h\n\t%prog -v -i sinlov/fastEncryptDecode\n' + DocHeadGithubCiGolang.hint_help_info)
        self_parser.add_option('-v', dest='v_verbose', action="store_true",
                               help="see verbose",
                               default=False)
        self_parser.add_option('-f', '--targetFile', dest='f_targetFile', type="string",
                               help="target file default is README.md",
                               default="README.md",
                               metavar="README.md")
        self_parser.add_option('-l', '--listFile', dest='l_listFile', type="string",
                               help="target file list use , to add",
                               default="",
                               metavar="README.md,README_ZH.md")
        self_parser.add_option('-i', '--infoGithub', dest='i_infoGithub', type="string",
                               help="info of github like",
                               default="",
                               metavar="sinlov/fastEncryptDecode")
        # self_parser.add_option('-c', '--clean', dest='c_clean', action="store_true",
        #                        help="clean after cli",
        #                        default=False)
        self.options, self.args = self_parser.parse_args()

    def opt(self):
        return self.options

    def verification_info_git_hub(self):
        if not self.options.i_infoGithub:
            exit('ERROR!must use -i or --infoGithub=!')

    def verification(self):
        if not self.options.f_targetFile or not self.options.c_clean:
            exit('ERROR!must support --clean and --targetFile parameters!')


def gen_doc_head_of_github_ci_golang_by_file(target_file, github_info):
    PLog.log("add head file is: {0}, info is {1}".format(target_file, github_info), 'd')
    if not os.path.exists(target_file):
        PLog.log('Err: want add target file not exist {}'.format(target_file), 'e', True)
        exit(1)
    new_head_content = ci_head_content % (github_info, github_info, github_info,
                                          github_info, github_info, github_info,
                                          github_info, github_info)
    PLog.log("new content is: {0}".format(new_head_content), 'd')


def gen_doc_head_of_github_ci_golang_by_list(file_list, github_info):
    pass


if __name__ == '__main__':
    PLog.check_runtime()
    if len(sys.argv) < 2:
        PLog.log(DocHeadGithubCiGolang.enter_error_info, 'e', True)
        exit(1)
    opt = DocHeadGithubCiGolang()

    # --infoGithub check
    opt.verification_info_git_hub()

    options = opt.opt()
    # --verbose
    if options.v_verbose:
        PLog.set_verbose(options.v_verbose)

    if options.l_listFile:
        gen_doc_head_of_github_ci_golang_by_list(options.l_listFile, options.i_infoGithub)
    else:
        gen_doc_head_of_github_ci_golang_by_file(options.f_targetFile, options.i_infoGithub)
