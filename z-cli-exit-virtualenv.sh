#!/usr/bin/env bash

shell_run_path=$(cd `dirname $0`; pwd)
shell_now_path_folder=$(pwd | awk -F "/" '{print $(NF)}')

prod_virtualenv_name="${shell_now_path_folder}"

checkFuncBack(){
  if [ ! $? -eq 0 ]; then
  	echo -e "\033[;31mRun [ $1 ] error exit code 1\033[0m"
    exit 1
  # else
    # echo -e "\033[;30mRun [ $1 ] success\033[0m"
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

checkUserAsRoot(){
  if [[ "$USER" != "root" ]]; then
    echo -e "\033[;31mMust run as root\033[0m"
    exit 1
  fi
}

# checkUserAsRoot


checkEnv virtualenv

source deactivate

echo -e "\033[;32m=> Exit virtualenv [ ${prod_virtualenv_name} ] success\033[0m"