## Percona Utils
this utility will help you to install and unsitall percona db using helm charts
we are using this repository  "https://github.com/percona/percona-helm-charts/tree/main/charts/pxc-db" for percona  installation 1.14.0 

### Prerequisites
* Python 3 should be installed on the machine from where you are running this script.

### How to use the script

### Supported Actions
You can pass `-h` flag to percona-utils script to get help
```shell
./percona-utils.sh -h
```

#### Install
To install you may pass following parameters:
* -a Action to perform (install or uninstall) (Default: install)
* -r Helm release name (mandatory)
* -n Helm release namespace (Default: default)
* -t PXC Image Tag (Default: 8.0.35-27.1)
* -s PXC Size (Default: 3)
* -v PXC Volume Size with unit, example: 1Gi or 1000Mi. (Default: 5Gi)
* -p  HA Proxy Size (Default: 1)
* -b  Backup Volume Size with unit, example: 1Gi or 1000Mi. (Default: 5Gi)
* -c  Volume Backup Schedule (Default: '0 0 * * *')
* -x  S3 Backup Schedule (Default: '0 0 * * 0')"

```shell
./percona-utils.sh -a install -r test-release -n test-ns -s 4
```

#### Uninstall
To uninstall you have to pass 3 paramters to the script as follows:
* -a uninstall
* -r release_name
* -n namespace


e.g.
```shell
./percona-utils.sh -a uninstall -r test-release -n test-ns
```

### How to Restore


```yaml
apiVersion: ps.percona.com/v1alpha1
kind: PerconaServerMySQLRestore
metadata:
  name: restore1
spec:
  clusterName: cluster1
  backupName: backup1
#  backupSource:
#    destination: s3://S3-BACKUP-BUCKET-NAME-HERE/backup-path
#    storage:
#      s3:
#        bucket: S3-BACKUP-BUCKET-NAME-HERE
#        credentialsSecret: cluster1-s3-credentials
#        region: us-west-2
#      type: s3
```