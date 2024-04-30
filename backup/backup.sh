#!/usr/bin/env bash

#OPTION 1
#release_name=""
#namespace="default"
#pxc_size="3"
#
#usage() {
#  echo "Usage: $0 --release release_name --namespace namespace --pxc_size 3"
#}
#
##TEMP=$(getopt -o r:n:s: --long release:,namespace:,pxc_size: -- "$@")
#
#if [ $? != 0 ]; then
#  echo "Terminating script..." >&2;
#  exit 1;
#fi
#
##eval set -- "$TEMP
#
#while true ; do
#  case "$1" in
#  -r|--release-name)
#    release_name=$2 ; shift 2 ;;
#  -n|--namespace)
#    namespace=$2 ; shift 2 ;;
#  -s|--pxc_size)
#    pxc_size=$2 ; shift 2 ;;
#  --) shift ; break ;;
#  *) echo "Error: Invalid Input" ; exit 1 ;;
#  esac
#done
#
#if [ -z ${release_name} ];then
#  echo "release_name is mandatory"
#  usage
#  exit 1
#fi
#
#echo "release_name = ${release_name}"
#echo "namespace = ${namespace}"
#echo "pxc_size = ${pxc_size}"

#OPTION 2
#read -p "Enter release name: " release_name
#read -p "Enter Namespace: " namespace

#OPTION 3
release_name="test"
namespace="testns"

python percona-install.py -r ${release_name} -n ${namespace}
