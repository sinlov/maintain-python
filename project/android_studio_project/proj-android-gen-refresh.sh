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

# checkEnv start
checkEnv java
checkEnv adb
checkEnv gradle
gradlew_path="${run_path}/gradlew"
if [ ! -f "${gradlew_path}" ]; then
    echo -e "\033[;31mFile ${gradlew_path} not find exit!\033[0m"
    exit 1
fi
if [ ! -x "${gradlew_path}" ]; then
    echo "this path gradlew not exec just try to fix!"
    chmod +x gradlew
fi
# checkEnv end

echo -e "\033[;32m${gradlew_path} -q generateReleaseSources --refresh-dependencies\033[0m"
${gradlew_path} -q generateReleaseSources --refresh-dependencies
