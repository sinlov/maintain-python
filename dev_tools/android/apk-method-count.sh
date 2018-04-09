#!/usr/bin/env bash

run_path=$(pwd)
shell_run_name=$(basename $0)
shell_run_path=$(cd `dirname $0`; pwd)
shell_now_path_folder=$(pwd | awk -F "/" '{print $(NF-1)}')

# setting temp for count
apk_temp="${shell_run_path}/dex_temp"
apk_zip_path="${apk_temp}/0.zip"

pV(){
    echo -e "\033[;36m$1\033[0m"
}
pI(){
    echo -e "\033[;32m$1\033[0m"
}
pD(){
    echo -e "\033[;34m$1\033[0m"
}
pW(){
    echo -e "\033[;33m$1\033[0m"
}
pE(){
    echo -e "\033[;31m$1\033[0m"
}
#pV "V"
#pI "I"
#pD "D"
#pW "W"
#pE "E"

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

checkEnv unzip
checkEnv hexdump

help_info="This shell can fast get apk method count when has CLI hexdump\n
	use	\033[;36m${shell_run_name} apkfile[0m
"

if [ $# == 0 ]; then
    pE "unknown params, please see help -h"
    exit 1
elif [ $# == 1 ]; then
    if [ $1 == "-h" ]; then
       echo -e ${help_info}
       exit 0
    fi
fi

apk_path=$1

if [[ ! -f ${apk_path} ]]; then
	pE "can not found apk path at => ${apk_path}"
	exit 1
fi

# mk temp folder for chekc apk temp
if [[ -d ${apk_temp} ]]; then
	pI "rm -rf ${apk_temp}"
	rm -rf ${apk_temp}
fi
mkdir ${apk_temp}

# cp file to temp folder
cp ${apk_path} ${apk_temp}

# get temp apk name
apk_name="$(basename ${apk_temp}/*.apk)"
# pD "apk_name => ${apk_name}"
# rename and unzip
mv ${apk_temp}/${apk_name} ${apk_zip_path}
unzip -t ${apk_zip_path} > /dev/null
checkFuncBack "unzip -t ${apk_zip_path}"
unzip -x ${apk_zip_path} -d ${apk_temp} > /dev/null

# found each method count
method_count_full=0
dex_file_list=$(find ${apk_temp} -name "*.dex")
for dex_file in ${dex_file_list} ; do
	dex_file_name=$(basename ${dex_file})
	# this script use dex file 92 method mark
	method_count_this=$(cat ${dex_file} | head -c 92 | tail -c 4 | hexdump -e '1/4 "%d\n"')
	echo -e "Dex => ${dex_file_name} [ ${method_count_this} ]"
	method_count_full=$(expr ${method_count_full} + ${method_count_this})
done
pI "Dex => [ ${apk_name} ] Method count is [ ${method_count_full} ]"
echo -e ${method_count_full}
# clean temp folder
rm -rf ${apk_temp}
