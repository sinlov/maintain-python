#!/usr/bin/env bash

run_path=$(pwd)
shell_run_name=$(basename $0)
shell_run_path=$(cd `dirname $0`; pwd)

build_tag="Sinlov-App"
build_module_name="test"

build_product_flavors=
build_product_flavors[0]="dev"
build_product_flavors[1]="prod"
#build_product_flavors[2]="test"

# default settings
build_module_folder="build/outputs/apk"
version_file="${shell_run_path}/gradle.properties"
android_build_type="debug"
build_alias=""
is_force_build=0
only_product_flavors_build=

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
#  else
#    echo -e "\033[;32mCli [ $1 ] event check success\033[0m\n-> \033[;34m$1 at Path: ${evn_checker}\033[0m"
  fi
}

check_count_apk_for_rename(){
    if [ -d "${shell_run_path}/${build_module_name}/${build_module_folder}" ]; then
        rename_apk_count=$(find "${shell_run_path}/${build_module_name}/${build_module_folder}" -name "*.apk" | wc -l | awk 'gsub(/^ *| *$/,"")')
        pI "Find Out build Apk Count: ${rename_apk_count}\n"
    else
        pE "can not find outputs apk!"
        exit 1
    fi
}

rename_apk_by_module(){
    apk_file_list=
    if [ $# == 2 ]; then
        apk_file_list=$(find "${shell_run_path}/${build_module_name}/${build_module_folder}" -name "*$1-*$2.apk")
    else
        apk_file_list=$(find "${shell_run_path}/${build_module_name}/${build_module_folder}" -name "*$1.apk")
    fi
    if [ ! -n "${apk_file_list}" ]; then
        pE "can not found apk build for setting rename exit"
        exit 1
    else
        for apk_path in ${apk_file_list};
        do
            now_time=$(date "+%Y-%m-%d-%H-%M")
            new_tag="${now_time}__$RANDOM"
            new_name=
            if [ ! -n "${build_alias}" ]; then
                new_name="${shell_run_path}/${build_module_name}/${build_module_folder}/${build_tag}-${project_version_name}-$1-${new_tag}.apk"
            else
                new_name="${shell_run_path}/${build_module_name}/${build_module_folder}/${build_tag}-${build_alias}-${project_version_name}-$1-${new_tag}.apk"
            fi
            pV "From apk: ${apk_path} \nToNewApk: ${new_name}"
            mv "${apk_path}" "${new_name}"
        done
    fi
}

help_info="This script \033[;34m${shell_run_name}\033[0m can rename android build apk\n
\n
\t-h see help\n
You can use \033[;32m ${shell_run_name} -t debug\033[0m\n
\n
More configuration\n
\t-t [buildType] set \033[;33mDefault build type is ${android_build_type}\033[0m\n
\t\t[buildType]\033[;32m only use debug release\033[0m\n
\t-p productFlavors \033[;36m ${shell_run_name} do only this productFlavors tasks\033[0m\n
\t-a alias \033[;36m ${shell_run_name} -a add alias of apk\033[0m\n
\t-f force \033[;36m ${shell_run_name} -f force do rename not check\033[0m\n
"


if [ $# == 0 ]; then
    pE "unknown params, please see help -h"
    exit 1
elif [ $# == 1 ]; then
    if [ $1 == "-h" ]; then
       echo -e ${help_info}
       exit 0
    fi
else
    while getopts "hft:p:a:" arg #after param has ":" need option
    do
        case ${arg} in
            h)
                echo -e ${help_info}
                exit 0
            ;;
            f)
                is_force_build=1
            ;;
            t)
                echo -e "-> Set build type is [ \033[;32m${OPTARG}\033[0m ]"
                if [ ${OPTARG} == "debug" ]; then
                    android_build_type="debug"
                elif [ ${OPTARG} == "release" ]; then
                    android_build_type="release"
                else
                    pE "Build type is not support [ ${OPTARG} ]"
                    echo -e "Only support\033[;33m ( debug release )\033[0m"
                    exit 1
                fi
            ;;
            p)
                echo -e "=> Set productFlavors only is [ \033[;32m${OPTARG}\033[0m ]"
                only_product_flavors_build=${OPTARG}
            ;;
            a)
                build_alias=${OPTARG}
            ;;
        esac
    done
fi

if [ ! -f "${version_file}" ]; then
    pE "can not found version_file as\n=> ${version_file}\nExit build"
    exit 1
fi


# get from ${version_file}
version_name_line=`cat ${version_file} | grep VERSION_NAME=`
versionNameTmp=`echo ${version_name_line#*\"}`
versionNameStr=`echo ${versionNameTmp%\"*}`
version_code_line=`cat gradle.properties | grep VERSION_CODE=`
versionCodeTmp=`echo ${version_code_line#*\"}`
versionCodeStr=`echo ${versionCodeTmp%\"*}`
# slice lines
OLD_IFS="$IFS"
IFS="="
version_name_arr=(${versionNameStr})
version_code_arr=(${versionCodeStr})
IFS="$OLD_IFS"
project_version_name=${version_name_arr[1]}
project_version_code=${version_code_arr[1]}
# check version
if [ ! -n "${project_version_name}" ]; then
    pE "In ${version_file} line VERSION_NAME set is empty exit build"
    exit 1
fi

if [ ! -n "${project_version_code}" ]; then
    pE "In ${version_file} line VERSION_CODE set is empty exit build"
    exit 1
fi

module_len=${#build_product_flavors[@]}
if [ ${module_len} -le 0 ]; then
    echo "you set [ build_product_flavors ] size is 0"
    exit 1
fi

echo -e "Now Rename Info\n
\tBuild Tag: ${build_tag}
\tModule_name: ${build_module_name}
\tProduct_flavors set: ${build_product_flavors[@]}
\tOnly_product_flavors_build: ${only_product_flavors_build}
\tAndroid_build_type: ${android_build_type}
\tVersionName: ${project_version_name}
\tVersionCode: ${project_version_code}
\n"

check_count_apk_for_rename

if [ -n "${only_product_flavors_build}" ]; then
    pI "You set -p build productFlavors is ${only_product_flavors_build}"
    rename_apk_by_module "${only_product_flavors_build}" ${android_build_type}
else
    if [ ! -n "${build_product_flavors}" ]; then
        pI "You set script build_product_flavors is Empty, so do simple rename"
        rename_apk_by_module ${android_build_type}
    else
        pI "-> rename apk build mode: ${android_build_type} by script build_product_flavors set"
        for product_flavor in ${build_product_flavors[@]};
        do
            echo "-> rename apk product_flavor name: ${product_flavor}"
            rename_apk_by_module "${product_flavor}" ${android_build_type}
        done
    fi
fi

exit 0
