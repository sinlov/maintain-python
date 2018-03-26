#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sinlov'

import fnmatch
import os
import sys
import re

field_pattern = r"@BindView\((.*?)\) (.*?) (.*?);"
butter_pattern = r"\n(.*?)ButterKnife.bind\((.*?)\);"
butter_regex = re.compile(butter_pattern)


class Resources:
    def __init__(self):
        pass

    butter_replacement = ''
    space = ''
    suffix = ''
    support26 = False


def replace_content(match):
    # remove Access Modifiers for assignments inside methods
    splits = match.group(3).split(' ')
    variable_name = splits[1] if len(splits) > 1 else splits[0]
    # check if we need type casting
    # if resources.support26 is true, we only empty string that means no type casting
    # if the type is View, we don't need type casting, obviously
    should_type_cast = Resources.suffix or Resources.support26 or match.group(2) == 'View'
    suffix = Resources.suffix if should_type_cast else "({0}) {1}".format(match.group(2), Resources.suffix)
    # save text to replace ButterKnife.Bind. This replacement text is variable assignments.
    Resources.butter_replacement += "{0}{1} = {2}findViewById({3});\n".format(Resources.space, variable_name, suffix,
                                                                              match.group(1))
    return "{0} {1};".format(match.group(2), match.group(3))


def process_file(abs_path):
    f = open(abs_path, 'r')
    content = f.read()
    f.close()

    # check if the file use ButterKnife
    result = butter_regex.search(content)
    if result:
        # indentation that needs for variable assignment statements
        Resources.space = result.group(1)
        # check if we need to add "view.".
        # In activity, we don't need it.
        # If the ButterKnife.bind has two arg_vs, that means it's not activity
        arg_vs = result.group(2).split(',')
        Resources.suffix = arg_vs[1].strip() + "." if len(arg_vs) > 1 else ""
        # re init age butter_replacement for next file
        Resources.butter_replacement = '\n\n'
        # replace fields
        content = re.sub(field_pattern, replace_content, content)
        # replace ButterKnife.Bind with variable assignments
        content = re.sub(butter_pattern, Resources.butter_replacement, content)
        print 'process file {0}\n'.format(abs_path)
        f = open(abs_path, 'w')
        f.write(content)
        f.close()


def search_over_java_file(file_dir):
    for root, dir_names, file_names in os.walk(file_dir):
        for filename in fnmatch.filter(file_names, '*.java'):
            abs_path = os.path.join(root, filename)
            process_file(abs_path)
        for dir_name in dir_names:
            search_over_java_file(dir_name)


if __name__ == '__main__':
    print('')
    if len(sys.argv) > 1:
        # check if there's an argv to command omitting type casting
        if len(sys.argv) > 2:
            Resources.support26 = sys.argv[2] == '26'
        search_over_java_file(sys.argv[1])
    else:
        search_over_java_file('.')
