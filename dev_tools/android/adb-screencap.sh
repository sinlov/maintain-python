#!/usr/bin/env bash

run_path=$(pwd)
shell_run_name=$(basename $0)
shell_run_path=$(cd `dirname $0`; pwd)
shell_now_path_folder=$(pwd | awk -F "/" '{print $(NF-1)}')
out_screen_path=

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

checkEnv adb

if [ ! -n "$1" ]; then
	out_screen_path="${run_path}/screen_$(date +%Y%m%d_%H%M_%S).png"
else
	out_screen_path=$1
fi

if [ ! -n ${out_screen_path} ]; then
	echo "error, your out screen path is empty"
	exit 1
fi

echo "out screencap path is ${out_screen_path}"

adb shell screencap -p /sdcard/temp.png
sleep 3
adb pull /sdcard/temp.png ${out_screen_path}
adb shell rm /sdcard/temp.png
echo "Get screencap success"
file ${out_screen_path}
exit 0