#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform
import optparse

import re

__author__ = 'sinlov'

is_verbose = False
level_set = 1
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


def text_replace(t_file, old_str=str, new_str=str):
    # type: (str, str, str) -> None
    if not os.path.exists(t_file):
        PLog.log('text_replace error file not exists => %s' % t_file, 'e', True)
        return
    try:
        lines = open(t_file, 'r').readlines()
        file_len = len(lines) - 1
        for i in range(file_len):
            if old_str in lines[i]:
                lines[i] = lines[i].replace(old_str, new_str)
        open(t_file, 'w').writelines(lines)
        PLog.log('replace_text success Path: %s | from => %s To => %s' % (t_file, old_str, new_str), '')
    except Exception as e:
        PLog.log('replace_text error %s' % str(e), 'e', True)


def text_remove_full_line(t_file, line_nums=[]):
    # type: (str, list) -> None
    if not os.path.exists(t_file):
        PLog.log('text_remove_full_line error file not exists => %s' % t_file, 'e', True)
        return
    if len(line_nums) == 0:
        PLog.log('text_remove_full_line line_num len is 0 => %s' % line_nums, '')
        return
    try:
        line_nums = list(set(line_nums))
        file_lines = open(t_file, 'r').readlines()
        file_len = len(file_lines)
        for line_num in line_nums:
            if line_num <= file_len:
                file_lines.remove(file_lines[line_num])
        open(t_file, 'w').writelines(file_lines)
        PLog.log('text_remove_full_line success Path: %s | line => %s' % (t_file, line_nums), '')
    except Exception as e:
        PLog.log('text_remove_full_line error %s' % str(e), 'e', True)


def text_replace_full_line(t_file, line_num=[], new_str=str):
    # type: (str, list, str) -> None
    if not os.path.exists(t_file):
        PLog.log('text_replace_full_line error file not exists => %s' % t_file, 'e', True)
        return
    if len(line_num) == 0:
        PLog.log('line_num len is 0 => %s' % line_num, '')
        return
    try:
        lines = open(t_file, 'r').readlines()
        file_len = len(lines)
        for line in line_num:
            for i in range(file_len):
                if line == i:
                    lines[i] = new_str
        open(t_file, 'w').writelines(lines)
        PLog.log('replace_text success Path: %s | line => %s as => %s' % (t_file, line_num, new_str), '')
    except Exception as e:
        PLog.log('replace_text error %s' % str(e), 'e', True)


def text_line_find(t_file=str, t_string=str):
    # type: (str, str, str) -> list
    res = []
    if not os.path.exists(t_file):
        return res
    else:
        try:
            f_lines = open(t_file, 'r').readlines()
            for line_num in range(len(f_lines)):
                if t_string in f_lines[line_num]:
                    res.append(line_num)
            return res
        except Exception as e:
            PLog.log('text_line_find error %s' % str(e), 'e', True)
            pass


def text_insert_line(t_file=str, line_no_s=[], insert_string=str):
    # type: (str, list, str) -> None
    """
    Insert several string to lines with line_no_s.
    """
    if not os.path.exists(t_file):
        PLog.log('text_line_find error file not exists => %s' % t_file, 'e', True)
        return
    if len(line_no_s) == 0:
        PLog.log('line_no_s len is 0 => %s' % line_no_s, '')
        return
    try:
        p_file = file(t_file)
        lines = []
        for line in p_file:
            lines.append(line)
        p_file.close()
        line_no_s = list(set(line_no_s))
        for line_in in line_no_s:
            lines.insert(line_in, insert_string)
        out_line_list = ''.join(lines)
        o_file = file(t_file, 'w')
        o_file.write(out_line_list)
        o_file.close()
    except Exception as e:
        PLog.log('text_insert error %s' % str(e), 'e', True)


class GradleCode:
    """
    for gradle Reg
    """

    def __init__(self):
        pass

    LINE_LOG = 128
    BUILD_GRADLE_BASE_NAME = r'build.gradle'
    DISTRIBUTION_URL = r'https\://services.gradle.org/distributions/gradle-4.1-all.zip'
    ANDROID_TOOLS_BUILD = "classpath 'com.android.tools.build:gradle:3.0.1'\n".rjust(57, ' ')
    REPOSITORIES_GOOGLE = "google()\n".rjust(17, ' ')
    REG_SETTING_GRADLE_START = r'^(\s*)(include).*$'
    REG_SETTING_GRADLE_BASE_NAME = r'settings.gradle'
    FLAVOR_DIMENSIONS_CODE = 'flavorDimensions "versionCode"\n'.rjust(39, ' ')


def find_out_settings_gradle_module_name(update_path):
    dev_modules = []
    settings_gradle_path = os.path.join(update_path, GradleCode.REG_SETTING_GRADLE_BASE_NAME)
    if not os.path.exists(settings_gradle_path):
        return dev_modules
    else:
        try:
            settings_lines = open(settings_gradle_path, 'r').readlines()
            for each_line in settings_lines:
                if re.match(GradleCode.REG_SETTING_GRADLE_START, each_line):
                    findall = re.split('[\'\"]', each_line)
                    for find in findall:
                        if find.startswith(":"):
                            module_name = find.replace(':', '')
                            dev_modules.append(module_name)
        except Exception as e:
            PLog.log("check_settings_gradle error, error info %s" % str(e), 'e', True)
            dev_modules = []
        return dev_modules


def reduce_settings_gradle(update_path):
    modules = find_out_settings_gradle_module_name(update_path)
    if len(modules) == 0:
        PLog.log("Error your input path %s not found settings.gradle" % update_path, 'e', True)
        exit(1)
    else:
        return modules


def update_module_build_gradle(module_root_path):
    module_gradle_path = os.path.join(module_root_path, GradleCode.BUILD_GRADLE_BASE_NAME)
    if not os.path.exists(module_gradle_path):
        PLog.log('in module [ %s ] not found %s' % (module_root_path, GradleCode.BUILD_GRADLE_BASE_NAME), 'e', True)
    else:
        an_build_tools_lines = text_line_find(module_gradle_path, r'//    buildToolsVersion')
        if len(an_build_tools_lines) == 0:
            text_replace(module_gradle_path, r'buildToolsVersion', r'//    buildToolsVersion')
        text_replace(module_gradle_path, r'testCompile', r'testImplementation')
        text_replace(module_gradle_path, r'androidTestCompile', r'androidTestImplementation')
        text_replace(module_gradle_path, r'compile ', r'implementation ')
        text_replace(module_gradle_path, r'apt ', r'annotationProcessor ')
        apt_line_find = text_line_find(module_gradle_path, r"apply plugin: 'android-apt'")
        if len(apt_line_find) > 0:
            text_remove_full_line(module_gradle_path, apt_line_find)
        product_flavors = text_line_find(module_gradle_path, r'productFlavors {')
        if len(product_flavors) > 0:
            flavor_dimensions = text_line_find(module_gradle_path, r'flavorDimensions "versionCode"')
            if len(flavor_dimensions) == 0:
                default_config_lines = text_line_find(module_gradle_path, r'defaultConfig {')
                if len(default_config_lines) > 0:
                    default_config_line = default_config_lines[0]
                    default_config_line = default_config_line + 1
                    text_insert_line(module_gradle_path, [default_config_line],
                                     GradleCode.FLAVOR_DIMENSIONS_CODE)


def update_each_module(update_path):
    modules = reduce_settings_gradle(update_path)
    PLog.log('module is %s' % modules, "")
    for each_module in modules:
        module_root_path = os.path.join(update_path, each_module)
        PLog.log('module_root_path: %s' % module_root_path, '')
        update_module_msg = 'just find module [ %s ] just update' % each_module
        update_module_msg = update_module_msg.rjust(GradleCode.LINE_LOG, '=')
        PLog.log(update_module_msg, "i", True)
        update_module_build_gradle(module_root_path)


def update_root_build_gradle(update_path):
    build_gradle_root_path = os.path.join(update_path, GradleCode.BUILD_GRADLE_BASE_NAME)
    if not os.path.exists(build_gradle_root_path):
        PLog.log('root build.gradle [ %s ] not found %s' % (update_path, build_gradle_root_path), 'e',
                 True)
    else:
        build_tools_find_line = text_line_find(build_gradle_root_path, 'com.android.tools.build')
        if len(build_tools_find_line) > 0:
            text_replace_full_line(build_gradle_root_path, build_tools_find_line,
                                   GradleCode.ANDROID_TOOLS_BUILD)
        repositories_lines = text_line_find(build_gradle_root_path, 'repositories {')
        if len(repositories_lines) > 0:
            repositories_google_lines = text_line_find(build_gradle_root_path, 'google()')
            if len(repositories_google_lines) == 0:
                insert_google_line = []
                for repositories_line in repositories_lines:
                    repositories_line = repositories_line + 1
                    insert_google_line.append(repositories_line)
                text_insert_line(build_gradle_root_path, insert_google_line, GradleCode.REPOSITORIES_GOOGLE)


def update_gradle_wrapper(update_path):
    gradle_wrapper_path = os.path.join(update_path, 'gradle', 'wrapper', 'gradle-wrapper.properties')
    if not os.path.exists(gradle_wrapper_path):
        PLog.log('gradle wrapper [ %s ] not found %s' % (update_path, gradle_wrapper_path), 'e',
                 True)
    else:
        distribution_url_lines = text_line_find(gradle_wrapper_path, 'distributionUrl')
        if len(distribution_url_lines) > 0:
            text_replace_full_line(gradle_wrapper_path, distribution_url_lines,
                                   'distributionUrl=%s\n' % GradleCode.DISTRIBUTION_URL)


def update_as_project_2_to_3(update_path):
    if not os.path.exists(update_path):
        PLog.log("Error your input Folder %s is not exist" % update_path, 'e', True)
        exit(1)
    if os.path.isdir(update_path) < 1:
        PLog.log("Error your input path %s is not folder" % update_path, 'e', True)
        exit(1)
    update_msg = ('Just Start Update [ %s ]' % update_path).ljust(GradleCode.LINE_LOG, ' ')
    PLog.log(update_msg, "i", True)
    update_gradle_wrapper(update_path)
    update_root_build_gradle(update_path)
    update_each_module(update_path)
    update_msg = ('Update end [ %s ]' % update_path).ljust(GradleCode.LINE_LOG, ' ')
    PLog.log(update_msg, "i", True)


if __name__ == '__main__':
    PLog.check_runtime()
    folder_path = ''
    if len(sys.argv) < 2:
        PLog.log(enter_error_info, 'e', True)
        exit(1)
    parser = optparse.OptionParser('\n%prog ' + ' -p \n\tOr %prog <folder>\n' + hint_help_info)
    parser.add_option('-v', dest='v_verbose', action="store_true", help="see verbose", default=False)
    parser.add_option('-f', '--folder', dest='f_folder', type="string", help="path of folder Default is .",
                      default=".", metavar=".")
    parser.add_option('-l', '--level', dest='l_level', type="int", help="top level Default 7 now no use",
                      default=7, metavar=7)
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    if options.l_level is not None:
        level_set = options.l_level
    if options.f_folder is not None:
        folder_path = options.f_folder
        if folder_path == '.':
            folder_path = os.getcwd()
        update_as_project_2_to_3(folder_path)
