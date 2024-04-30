#!/usr/bin/env bash

ACTION="install"
RELEASE_NAME=""
NAMESPACE="default"
PXC_IMAGE_TAG="8.0.35-27.1"
PXC_SIZE="3"
PXC_VOLUME_SIZE="5Gi"
HAPROXY_SIZE="1"
BACKUP_VOLUME_SIZE="5Gi"
VOLUME_BACKUP_SCHEDULE="0 0 * * *" #Daily at 12 AM
S3_BACKUP_SCHEDULE="0 0 * * 0" #12 AM at every sunday

usage() {
  echo "Usage: $0 [-a action] [-r release_name] [-n namespace] [-s pxc_size] [-v pxc_volume_size]"
  echo " -a Action to perform (install or uninstall) (Default: install)"
  echo " -r Helm release name (mandatory)"
  echo " -n Helm release namespace (Default: default)"
  echo " -t PXC Image Tag (Default: 8.0.35-27.1)"
  echo " -s PXC Size (Default: 3)"
  echo " -v PXC Volume Size with unit, example: 1Gi or 1000Mi. (Default: 5Gi)"
  echo " -p  HA Proxy Size (Default: 1)"
  echo " -b  Backup Volume Size with unit, example: 1Gi or 1000Mi. (Default: 5Gi)"
  echo " -c  Volume Backup Schedule (Default: '0 0 * * *')"
  echo " -x  S3 Backup Schedule (Default: '0 0 * * 0')"
  exit 1
}


while getopts ":a:r:n:t:s:v:p:b:c:x:h" opt; do
  case "${opt}" in
    a )
      ACTION=$OPTARG
      ;;
    r )
      RELEASE_NAME=$OPTARG
      ;;
    n )
      NAMESPACE=$OPTARG
      ;;
    t )
      PXC_IMAGE_TAG=$OPTARG
      ;;
    s )
      PXC_SIZE=$OPTARG
      ;;
    v )
      PXC_VOLUME_SIZE=$OPTARG
      ;;
    p )
      HAPROXY_SIZE=$OPTARG
      ;;
    b )
      BACKUP_VOLUME_SIZE=$OPTARG
      ;;
    c )
      VOLUME_BACKUP_SCHEDULE=$OPTARG
      ;;
    x )
      S3_BACKUP_SCHEDULE=$OPTARG
      ;;
    h )
      HELP=$OPTARG
      usage
      ;;
    \? )
      usage
      ;;
  esac
done

shift $((OPTIND -1))


if [ -z ${RELEASE_NAME} ];then
  echo -e "Error: -r release_name is mandatory \n"
  usage
  exit 1
fi


# Install Helm Chart
if [ ${ACTION} == "install" ];then
  export  RELEASE_NAME NAMESPACE PXC_IMAGE_TAG PXC_SIZE PXC_VOLUME_SIZE HAPROXY_SIZE BACKUP_VOLUME_SIZE VOLUME_BACKUP_SCHEDULE S3_BACKUP_SCHEDULE
  python3 percona-install.py
fi

# Uninstall Helm Chart
if [ ${ACTION} == "uninstall" ];then
  helm uninstall ${RELEASE_NAME} -n ${NAMESPACE}
fi