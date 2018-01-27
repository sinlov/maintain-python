#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
import stat
import sys
import time
import optparse

__author__ = 'sinlov'

reload(sys)
sys.setdefaultencoding('utf-8')

is_verbose = False
is_force = False
is_idea = False
is_android_studio = False
is_android_free_line = False


def change_files_write(path=str):
    for root, dirs, files in os.walk(path):
        for name in files:
            os.chmod(os.path.join(root, name), stat.S_IWRITE)
    print ('change change_files_write success')


def del_files(path=str):
    try:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.startswith("."):
                    os.remove(os.path.join(root, name))
        print ("delete path " + path + " success!")
    except Exception, e:
        print e


def is_path_idea_project(p_path=str):
    for root, dirs, files in os.walk(p_path):
        for name in files:
            if name.endswith(".iml"):
                return True
    return False


def clean_idea_useless_code():
    global is_force, is_verbose, is_android_studio, is_android_free_line
    for root, dirs, files in os.walk(os.getcwd()):
        for name in dirs:
            if name.endswith(".idea"):
                verbose_print('Find .idea at {}/{}/'.format(root, name))
                shutil.rmtree(os.path.join(str(root), str(name)), is_force)
                time.sleep(1)
            if name.endswith("build"):
                verbose_print('Find build/ at {}/{}/'.format(root, name))
                shutil.rmtree(os.path.join(str(root), str(name)), is_force)
                time.sleep(1)
            if is_android_studio:
                if name.endswith(".gradle"):
                    find_folder_gradle = "Find .gradle/ " + str(root) + "/" + str(name) + "/"
                    verbose_print(find_folder_gradle)
                    shutil.rmtree(os.path.join(str(root), str(name)), is_force)
                    time.sleep(1)
            if is_android_free_line:
                if name.endswith("freeline"):
                    find_folder_gradle = "Find freeline " + str(root) + "/" + str(name) + "/"
                    verbose_print(find_folder_gradle)
                    shutil.rmtree(os.path.join(str(root), str(name)), is_force)
                    time.sleep(1)
        for name in files:
            if name.endswith(".iml"):
                find_file_iml = "Find iml at: " + str(root) + "/" + str(name)
                verbose_print(find_file_iml)
                os.remove(str(root) + "/" + str(name))


def clean_idea_build_files(dir_path=str):
    for root, dirs, files in os.walk(dir_path):
        for name in dirs:
            if name.endswith("build"):
                find_folder_build = "Find build/ " + str(root) + "/" + str(name) + "/"
                verbose_print(find_folder_build)
                shutil.rmtree((str(root) + "/" + str(name)), is_force)
                time.sleep(1)


def verbose_print(info=str):
    if is_verbose:
        print info


def fix_idea_project_at_root():
    if is_path_idea_project(os.getcwd()):
        path_start_clean = "Start clean project at " + str(os.getcwd())
        print  path_start_clean
        clean_idea_useless_code()
        path_end_clean = "End clean project at " + str(os.getcwd())
        print path_end_clean
        exit(0)
    else:
        path_error_str = "Can not find *.iml with this project at" + str(os.getcwd() + '\n\tAre you clean?')
        print path_error_str
        exit(1)


def clean_project_build_dir():
    path_start_clean = "Start clean project build File at " + str(os.getcwd())
    print  path_start_clean
    clean_idea_build_files(os.getcwd())
    path_end_clean = "End clean project build File at " + str(os.getcwd())
    print path_end_clean
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must input params or see -h"
        exit(1)
    check_p = str(sys.argv[1])
    if not check_p.startswith('-'):
        print 'You params is error please see -h'
        exit(1)
    parser = optparse.OptionParser('Usage %prog ' + '-i -v')
    parser.add_option('-v', dest='v_verbose', action="store_true", help="see verbose", default=False)
    parser.add_option('-i', dest='i_idea', action="store_true", help="clean idea project", default=False)
    parser.add_option('-a', dest='i_as', action="store_true", help="clean Android Studio", default=False)
    parser.add_option('--freeline', dest='i_free_line', action="store_true", help="clean Android free line",
                      default=False)
    parser.add_option('-b', dest='cleanBuild', action="store_true", help="clean all Build dir, only support -v params",
                      default=False)
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    if options.i_idea:
        is_idea = True
    if options.cleanBuild:
        clean_project_build_dir()
    else:
        if options.i_as:
            is_android_studio = True
        if options.i_free_line:
            is_android_free_line = True
        if is_idea or is_android_studio or is_android_free_line:
            fix_idea_project_at_root()
