#!/usr/bin/env bash

depend_conf_mode="implementation"

run_path=$(pwd)
shell_run_name=$(basename $0)
shell_run_path=$(cd `dirname $0`; pwd)

pV(){
    echo -e "\033[;36m$1\033[0m"
}
pI(){
    echo -e "\033[;32mINFO: $1\033[0m"
}
pD(){
    echo -e "\033[;34mDEBUG: $1\033[0m"
}
pW(){
    echo -e "\033[;33mWARN: $1\033[0m"
}
pE(){
    echo -e "\033[;31mERROR: $1\033[0m"
}

checkFuncBack(){
  if [ $? -ne 0 ]; then
    echo -e "\033[;31mRun [ $1 ] error exit code 1\033[0m"
    exit 1
  # else
  #   echo -e "\033[;30mRun [ $1 ] success\033[0m"
fi
}

checkBinary(){
    binary_checker=`which $1`
    checkFuncBack "which $1"
    if [[ ! -n "${binary_checker}" ]]; then
        echo -e "\033[;31mCheck binary [ $1 ] error exit\033[0m"
        exit 1
        #  else
        #    echo -e "\033[;32mCli [ $1 ] binary check success\033[0m\n-> \033[;34m$1 at Path: ${binary_checker}\033[0m"
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

function Usage(){
cat << HELP
Usage: ${shell_run_name} [moduleName]

Example:
  ${shell_run_name} app

Help:
  This ${shell_run_name} can fast see gradle project depends

  -m module set If set -m script will check module exist!
  -t task             show  ${shell_run_name} -m [moduleName] -t
  -b buildEnvironment mode  ${shell_run_name} -m [moduleName] -b
  -c compile          mode  ${shell_run_name} -m [moduleName] -c
  -r releaseCompile   mode  ${shell_run_name} -m [moduleName] -r
  -f full             mode  ${shell_run_name} -m [moduleName] -f
HELP
}

ARG=$1
if [[ "$ARG" =~ "-h" ]];then
    Usage
    exit 0
fi

# checkBinary
checkBinary java
checkBinary android
checkBinary gradle
checkRunPathGradlew

if [ $# == 0 ]; then
    echo "unknown params, please see help -h"
    exit 1
elif [ $# == 1 ]; then
    case $1 in
        "-b" )
            pI "=> buildEnvironment mode"
            ${run_path}/gradlew buildEnvironment
            exit 0
        ;;
        "-t" )
            pI "=> task mode"
            ${run_path}/gradlew task
            exit 0
        ;;
        * )
            pI "=> fast show module dependencies mode"
            reduceGradleModule $1
            runGradleDependenciesTask ${android_build_module} ${depend_conf_mode}
        ;;
        esac
else
    run_gradle_module=""
    other_module=""
    while getopts "hm:bcrft" arg #after param has ":" need option
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
            b)
                ${run_path}/gradlew buildEnvironment
                exit 0
            ;;
            c)
                pI "=> compile mode"
                depend_conf_mode="compile"
            ;;
            r)
                pI "=> releaseCompile mode"
                depend_conf_mode="releaseCompileClasspath"
            ;;
            f)
                pI "=> full mode at ${run_gradle_module}"
                other_module="dependencies"
            ;;
            t)
                pI "=> task show at ${run_gradle_module}"
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
