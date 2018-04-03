#!/usr/bin/env bash

shell_run_path=$(cd `dirname $0`; pwd)
shell_now_path_folder=$(pwd | awk -F "/" '{print $(NF)}')

prod_virtualenv_name="${shell_now_path_folder}"
want_install_modules=(
)


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

virtualenv --system-site-packages ${prod_virtualenv_name}

source ${prod_virtualenv_name}/bin/activate

if [ $# -eq 0 ]; then
    if [ -n "${want_install_modules}" ]; then
        for module in ${want_install_modules[@]};
        do
            echo -e "\033[;34m-> now install module [ ${module} ]\033[0m"
            pip install module
        done
    fi
    echo -e "\033[;36m=> If not want install module, please input any args\033[0m"
else
    echo -e "\033[;32m=> Not install any module!\033[0m"
fi

echo -e "\033[;32m=> Exec virtualenv [ ${prod_virtualenv_name} ] success\033[0m"