import subprocess


def add_helm_repo(name,url):
    subprocess.run(["helm", "repo", "add", name, url])
    subprocess.run(["helm", "repo", "update"])

def get_schedule(type):
    if type.lower() == "daily":
        return "0 0 * * *"
    elif type.lower() == "hourly":
        return "0 * * * *"
    elif type.lower() == "weekly":
        return "0 0 * * 0"
    return None

def install_percona(chart_ref):
    # Inputs
    environment_name = input("Enter the environment name (Default: test) (Allowed Values: test/prod) : ") or "test"
    release_name = input("Enter the release name: ")
    namespace = input("Enter the namespace: ")
    pxcSize = input("Enter PXC Size (default: 3): ") or "3"
    pxcStorageClass = input("Enter PXC Volume Storage Class Name (default: csi-rbd-sc): ") or "csi-rbd-sc"
    pxcStorageSize = input("Enter PXC Volume Storage Size (Default: 5Gi): ") or "5Gi"
    haproxySize = input("Enter HAProxy Size (default: 1): ") or "1"
    backupStorageClass = input("Enter Backup Volume Storage Class Name (default: csi-rbd-sc): ") or "csi-rbd-sc"
    backupStorageSize = input("Enter Backup Volume Storage Size (Default: 2Gi): ") or "2Gi"
    volumeBackupType = input("Enter Backup Schedule for volume backup (hourly/daily/weekly) (Default: daily): ") or "daily"
    s3BackupType = input("Enter Backup Schedule for s3 backup (hourly/daily/weekly) (Default: daily): ") or "daily"

    volumeBackupSchedule = get_schedule(volumeBackupType)
    s3BackupSchedule = get_schedule(s3BackupType)

    if environment_name == "test":
        backupBucket = "percona-backups-test"
    elif environment_name == "prod":
        backupBucket = "percona-backups"


#Helm Install
    subprocess.run(["helm", "upgrade", "--install", release_name, chart_ref,
                    "--namespace", namespace,
                    "--set", f"pxc.size={pxcSize}",
                    "--set", f"pxc.persistence.storageClass={pxcStorageClass}",
                    "--set", f"pxc.persistence.size={pxcStorageSize}",
                    "--set", f"haproxy.size={haproxySize}",
                    "--set", f"backup.storages.percona-backup.volume.persistentVolumeClaim.storageClassName={backupStorageClass}",
                    "--set", f"backup.storages.percona-backup.volume.persistentVolumeClaim.resources.requests.storage={backupStorageSize}",
                    "--set", f"backup.storages.ceph-s3-us-west.s3.bucket={backupBucket}",
                    "--set", f"backup.schedule[0].name=volume-backup",
                    "--set", f"backup.schedule[0].storageName=percona-backup-new",
                    "--set", f"backup.schedule[0].schedule={volumeBackupSchedule}",
                    "--set", f"backup.schedule[0].keep=5",
                    "--set", f"backup.schedule[1].name=s3-backup",
                    "--set", f"backup.schedule[1].storageName=ceph-s3-us-west",
                    "--set", f"backup.schedule[1].schedule={volumeBackupSchedule}",
                    "--set", f"backup.schedule[1].keep=5",
                    ])


if __name__ == '__main__':
    add_helm_repo("uvarc","https://uvarc.github.io/helm-charts/")
    install_percona("uvarc/pxc-db")