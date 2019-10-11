#!/usr/bin/env bash

info_tools_install_base_path="$HOME/opt/bin"
info_ninja_install_path="${info_tools_install_base_path}/ninja"
info_gn_install_path="${info_tools_install_base_path}/gn"

run_path=$(pwd)
shell_run_name=$(basename $0)
shell_run_path=$(cd `dirname $0`; pwd)
shell_now_path_folder=$(pwd | awk -F "/" '{print $(NF-1)}')

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

checkFuncBack(){
  if [[ $? -ne 0 ]]; then
    echo -e "\033[;31mRun [ $1 ] error exit code 1\033[0m"
    exit 1
  # else
  #   echo -e "\033[;30mRun [ $1 ] success\033[0m"
  fi
}

checkEnv(){
  evn_checker=`which $1`
  checkFuncBack "which $1"
  if [[ ! -n "${evn_checker}" ]]; then
    echo -e "\033[;31mCheck event [ $1 ] error exit\033[0m"
    exit 1
#  else
#    echo -e "\033[;32mCli [ $1 ] event check success\033[0m\n-> \033[;34m$1 at Path: ${evn_checker}\033[0m"
  fi
}

echo -e "This shell can install ninja and gn tools for build
    Must use cli git and https://github.com and https://gn.googlesource.coma
    If has error, please check your network.

    this script can install at ubuntu
"
checkEnv git


check_ninja=$(which ninja)
if [[ $? -ne 0 ]]; then
    pI "-> ninja not install, now install as https://github.com/ninja-build/ninja"
    if [[ ! -d ${info_ninja_install_path} ]];then
        pI "-> start download ninja"
        git clone https://github.com/ninja-build/ninja.git ${info_ninja_install_path}
        checkFuncBack "git clone https://github.com/ninja-build/ninja.git ${info_ninja_install_path}"
    fi
    cd ${info_ninja_install_path}
    git checkout release
    checkFuncBack "git checkout release"
    ./configure.py --bootstrap
    if [[ ${USER} == "root" ]]; then
        ln -s ${info_ninja_install_path}/ninja /usr/local/bin/ninja
    else
        pW "install ninja need sudo"
        sudo ln -s ${info_ninja_install_path}/ninja /usr/local/bin/ninja
    fi
    pI "=> now install ninja at ${info_ninja_install_path} link at /usr/local/bin/ninja"
    cd ${run_path}
else
    pI "-> has install ninja at ${check_ninja}"
fi

check_clang=$(which clang)
if [[ $? -ne 0 ]]; then
    pI "-> try to install clang"
    if [[ ${USER} == "root" ]]; then
        apt-get install -y clang
    else
        sudo apt-get install -y clang
    fi
else
    pI "-> has install clang at ${check_clang}"
fi

check_ninja=$(which ninja)
if [[ $? -ne 0 ]];then
    pI "-> try to install ninja"

fi
#git clone https://gn.googlesource.com/gn
#cd gn
#python build/gen.py
#ninja -C out
# add path gn/out to path