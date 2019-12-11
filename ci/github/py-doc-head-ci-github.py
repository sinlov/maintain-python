#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import optparse
import os
import platform
import re
import sys
import urllib2

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    # print('change encoding error {}'.format(e))
    pass


class CiHead:
    golang = r"""[![TravisBuildStatus](https://api.travis-ci.org/%s.svg?branch=master)](https://travis-ci.org/%s)
[![GoDoc](https://godoc.org/github.com/%s?status.png)](https://godoc.org/github.com/%s/)
[![GoReportCard](https://goreportcard.com/badge/github.com/%s)](https://goreportcard.com/report/github.com/%s)
[![codecov](https://codecov.io/gh/%s/branch/master/graph/badge.svg)](https://codecov.io/gh/%s)
"""
    golang_doc_head_match = r'^\s*\[\!\[(TravisBuildStatus|GoDoc|GoWalkerDoc|GoReportCard|codecov)\].*$'

    nodejs = r"""[![TravisBuildStatus](https://api.travis-ci.org/%s.svg?branch=master)](https://travis-ci.org/%s)
[![codecov](https://codecov.io/gh/%s/branch/master/graph/badge.svg)](https://codecov.io/gh/%s)
"""
    nodejs_doc_head_match = r'^\s*\[\!\[(TravisBuildStatus|codecov)\].*$'

    def __init__(self):
        pass


class GithubApi:
    base_url = 'https://api.github.com'
    repos = '/repos'
    repos_languages = '/languages'

    def __init__(self):
        pass


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


def differ_file_list_by_option_to_gen(option):
    if option.l_listFile:
        return str(options.l_listFile).split(',')
    else:
        return [option.f_targetFile]


def urllib_request_json_dict_get(github_repo_url):
    # type: (str) -> dict
    try:
        req = urllib2.Request(github_repo_url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        json_disc = json.loads(res)
        return json_disc
    except Exception as urllib_request_json_get_err:
        PLog.log(
            'urllib_request_json_dict_get error {0}\nErr url: {1}'.format(urllib_request_json_get_err, github_repo_url),
            'e')
        return {}


def check_file_list_and_project_github_info(github_project_full_name, is_force, target_file_list):
    if len(target_file_list) < 1:
        PLog.log('Err: target file not set', 'e', True)
        return False
    if not check_github_project_by_full_name(github_project_full_name):
        PLog.log('-> warning github project full name [ {0} ] not found'.format(github_project_full_name), 'w')
        if not is_force:
            PLog.log(DocHeadGithubCi.msg_interrupt_generate, 'w')
            return False
    return True


def check_github_project_by_full_name(github_full_name):
    github_repo_url = '{0}{1}/{2}'.format(GithubApi.base_url, GithubApi.repos, github_full_name)
    github_repo_languages_url = '{0}{1}'.format(github_repo_url, GithubApi.repos_languages)
    try:
        repo_info = urllib_request_json_dict_get(github_repo_url)
        PLog.log('=> github_repo_url {0}'.format(github_repo_url), 'd')
        if repo_info:
            PLog.log('content=\n{0}'.format(json.dumps(repo_info)), 'd')
            if not repo_info.has_key('full_name'):
                PLog.log('can not found repo by full_name: {0} , please check'.format(github_full_name), 'w', True)
                return False
            if repo_info['full_name'] != github_full_name:
                PLog.log('checked full_name is {0}, want {1}'.format(repo_info['full_name'], github_full_name), 'w',
                         True)
                return False
            repo_languages = urllib_request_json_dict_get(github_repo_languages_url)
            PLog.log("=> github project info\n"
                     "  full_name: {0}\n"
                     "  html_url: {1}\n"
                     "  description{2}\n"
                     "  fork: {3}\n"
                     "  created_at: {4}\n"
                     "  updated_at: {5}\n"
                     "  languages: {6}\n"
                     "  ssh_url: {7}\n"
                     .format(repo_info['full_name'],
                             repo_info['html_url'],
                             repo_info['description'],
                             repo_info['fork'],
                             repo_info['created_at'],
                             repo_info['updated_at'],
                             json.dumps(repo_languages),
                             repo_info['ssh_url'],
                             ), 'i', True)
            return True
        else:
            return False
    except Exception as check_repo_err:
        PLog.log('check_github_project_by_full_name error {}'.format(check_repo_err), 'e')
        return False


def replace_file_list_with_new_content(type_name, target_file_list, github_project_full_name, new_head,
                                       match_content):
    try:
        for target_file in target_file_list:
            if not os.path.exists(target_file):
                PLog.log('Err: want add target file not exist {}'.format(target_file), 'e', True)
                exit(1)
            new_line = [new_head]
            with open(target_file, 'r') as doc_file:
                read_lines = doc_file.readlines()
                for line in read_lines:
                    if re.match(match_content, line):
                        continue
                    new_line.append(line)
            with open(target_file, 'w') as refresh_file:
                refresh_file.writelines(new_line)
            PLog.log("=> add head file is: {0}, "
                     "github full link: https://github.com/{1}".format(target_file,
                                                                       github_project_full_name),
                     'i', True)
    except Exception as err:
        PLog.log('gen_doc_head_of_github_ci {0} file error {1}'.format(type_name, err), 'e')


def gen_doc_head_of_github_ci_golang_by_file(target_file_list, github_project_full_name, is_force):
    if not check_file_list_and_project_github_info(github_project_full_name, is_force, target_file_list):
        exit(1)
    new_head_content = CiHead.golang % (
        github_project_full_name, github_project_full_name,
        github_project_full_name, github_project_full_name,
        github_project_full_name, github_project_full_name,
        github_project_full_name, github_project_full_name)
    PLog.log("=> new content is: {0}".format(new_head_content), 'd')
    replace_file_list_with_new_content(type_name='golang',
                                       target_file_list=target_file_list,
                                       github_project_full_name=github_project_full_name,
                                       new_head=new_head_content, match_content=CiHead.golang_doc_head_match)


def gen_doc_head_of_github_ci_nodejs_by_file(target_file_list, github_project_full_name, is_force):
    if not check_file_list_and_project_github_info(github_project_full_name, is_force, target_file_list):
        exit(1)
    new_head_content = CiHead.nodejs % (
        github_project_full_name, github_project_full_name,
        github_project_full_name, github_project_full_name)
    PLog.log("=> new content is: {0}".format(new_head_content), 'd')
    replace_file_list_with_new_content(type_name='nodejs',
                                       target_file_list=target_file_list,
                                       github_project_full_name=github_project_full_name,
                                       new_head=new_head_content, match_content=CiHead.nodejs_doc_head_match)


class DocHeadGithubCi:
    hint_help_info = """
python cli tools for generate github Top document temple for different language
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
    msg_interrupt_generate = 'generate interrupt, if you want to continue use --force'

    def __init__(self):
        self.options = None
        self.args = None
        self_parser = optparse.OptionParser(
            '\n\t%prog' + ' -h\n\t%prog -g sinlov/fastEncryptDecode\n' + DocHeadGithubCi.hint_help_info)
        self_parser.add_option('-v', dest='v_verbose', action="store_true",
                               help="see verbose",
                               default=False)
        self_parser.add_option('--force', dest='force', action="store_true",
                               help="do job force, ignore warning",
                               default=False)
        self_parser.add_option('-f', '--targetFile', dest='f_targetFile', type="string",
                               help="target file default is README.md, if set --listFile will ignore this option",
                               default="README.md",
                               metavar="README.md")
        self_parser.add_option('-l', '--listFile', dest='l_listFile', type="string",
                               help="target file list to generate, this option will cover --targetFile",
                               default="",
                               metavar="README.md,README_ZH.md")
        self_parser.add_option('-g', '--golang', dest='g_golang', type="string",
                               help="generate golang project use travis-ci doc and so on.",
                               default="",
                               metavar="sinlov/fastEncryptDecode")
        self_parser.add_option('--nodejs', dest='nodejs', type="string",
                               help="generate nodejs project use travis-ci doc and so on.",
                               default="",
                               metavar="bridgewwater/webpack-project-temple-base")
        self.options, self.args = self_parser.parse_args()

    def opt(self):
        return self.options

    def args(self):
        return self.args


if __name__ == '__main__':
    PLog.check_runtime()
    if len(sys.argv) < 2:
        PLog.log(DocHeadGithubCi.enter_error_info, 'e', True)
        exit(1)
    opt = DocHeadGithubCi()

    options = opt.opt()
    # --verbose
    if options.v_verbose:
        PLog.set_verbose(options.v_verbose)

    # --force
    if options.force:
        PLog.log(DocHeadGithubCi.msg_open_force_mode, 'w')

    # --targetFile or --listFile
    target_files = differ_file_list_by_option_to_gen(options)

    # --golang
    if options.g_golang:
        gen_doc_head_of_github_ci_golang_by_file(target_files, options.g_golang,
                                                 options.force)
    # --nodejs
    if options.nodejs:
        gen_doc_head_of_github_ci_nodejs_by_file(target_files, options.nodejs,
                                                 options.force)
