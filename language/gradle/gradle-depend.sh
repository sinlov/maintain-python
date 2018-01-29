#!/usr/bin/env bash

run_path=$(pwd)
shell_run_name=$(basename $0)
shell_run_path=$(cd `dirname $0`; pwd)

checkFuncBack(){
  if [ $? -ne 0 ]; then
    echo -e "\033[;31mRun [ $1 ] error exit code 1\033[0m"
    exit 1
  # else
  #   echo -e "\033[;30mRun [ $1 ] success\033[0m"
fi
}

checkEnv(){
  evn_checker=`which $1`
  checkFuncBack "which $1"
  if [ ! -n "evn_checker" ]; then
    echo -e "\033[;31mCheck event [ $1 ] error exit\033[0m"
    exit 1
  # else
  #   echo -e "\033[;32mCli [ $1 ] event check success\033[0m\n-> \033[;34m$1 at Path: ${evn_checker}\033[0m"
fi
}

checkRunPathGradlew(){
  if [ ! -f "${run_path}/gradlew" ]; then
    echo "this path gradlew not exist!"
    exit 1
  fi

  if [ ! -x "${run_path}/gradlew" ]; then
    echo "this path gradlew not exec just try to fix!"
    chmod +x gradlew
#  else
#    echo "=> local gradlew can use"
  fi
}

android_build_module=
reduceGradleModule(){
    android_build_module=":"
    if [[ -n "$1" ]]; then
        if [[ ! -d "${run_path}/$1" ]]; then
            echo -e "\033[;31mCan not find module at ${run_path}/$1\033[0m"
            exit 1
        fi
        android_build_module="$1:"
    else
        android_build_module=""
    fi
}

runGradleDependenciesTask(){
    if [ $# != 2 ]; then
        echo -e "\033[;31m runGradleDependenciesTask must has 2 params\033[0m"
        exit 1
    fi
    echo -e "${run_path}/gradlew -q $1dependencies --configuration $2"
    ${run_path}/gradlew -q "$1dependencies" --configuration "$2"
}

# checkEnv
checkEnv java
checkEnv android
checkEnv gradle
checkRunPathGradlew

depend_conf_mode="implementation"

help_info="This gradle-depend.sh can fast see gradle project depends\n
\t-h see help\n
\n
Fast see mode ${depend_conf_mode}\n
\t You can use \033[;34m gradle-depend.sh [moduleName]\033[0m\n
\n
If want other mode can use as\n
\t-m module set \033[;32mIf set -m script will check module exist! \033[0m\n
\t-c compile mode \033[;36m gradle-depend.sh -m [moduleName] -c\033[0m\n
\t-r runtime mode \033[;36m gradle-depend.sh -m [moduleName] -r\033[0m\n
\t-f full mode \033[;36m gradle-depend.sh -m [moduleName] -f\033[0m\n
\t-t task show \033[;36m gradle-depend.sh -m [moduleName] -t\033[0m\n
"

if [ $# == 0 ]; then
    echo "unknown params, please see help -h"
    exit 1
elif [ $# == 1 ]; then
    if [ $1 == "-h" ]; then
       echo -e ${help_info}
    else
       reduceGradleModule $1
       runGradleDependenciesTask ${android_build_module} ${depend_conf_mode}
    fi
else
    run_gradle_module=""
    other_module=""
    while getopts "hm:crft" arg #after param has ":" need option
    do
        case $arg in
            h)
                echo -e ${help_info}
                exit 0
            ;;
            m)
                reduceGradleModule ${OPTARG}
                run_gradle_module=${android_build_module}
            ;;
            c)
                depend_conf_mode="compile"
            ;;
            r)
                depend_conf_mode="runtime"
            ;;
            f)
                other_module="dependencies"
            ;;
            t)
                other_module="tasks"
            ;;
        esac
    done
    if [ -n "${other_module}" ]; then
        echo -e "${run_path}/gradlew -q ${run_gradle_module}${other_module}"
        ${run_path}/gradlew -q "${run_gradle_module}${other_module}"
    else
        runGradleDependenciesTask ${run_gradle_module} ${depend_conf_mode}
    fi
fi
