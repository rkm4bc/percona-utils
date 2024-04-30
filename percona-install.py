import subprocess
import os

def add_helm_repo(name, url):
    subprocess.run(["helm", "repo", "add", name, url])
    subprocess.run(["helm", "repo", "update"])

def install_percona(chart_ref, chart_version):
    #Helm Install
    subprocess.run([
        "helm", "upgrade", "--install", str(os.environ.get('RELEASE_NAME')),
        chart_ref, "--namespace", str(os.environ.get('NAMESPACE', 'default')),
        "--version", chart_version,
        "--set", f"pxc.image.tag=" + str(os.environ.get('PXC_IMAGE_TAG', '8.0.35-27.1')),
        "--set", f"pxc.size=" + str(os.environ.get('PXC_SIZE', 3)),
        "--set", f"pxc.persistence.size=" + str(os.environ.get('PXC_VOLUME_SIZE', '5Gi')),
        "--set", f"haproxy.size=" + str(os.environ.get('HAPROXY_SIZE', '1')),
        "--set", f"backup.storages.percona-backup.volume.persistentVolumeClaim.resources.requests.storage=" + str(os.environ.get('BACKUP_VOLUME_SIZE', '5Gi')),
        "--set", f"backup.schedule[0].name=volume-backup",
        "--set", f"backup.schedule[0].storageName=percona-backup",
        "--set", f"backup.schedule[0].schedule=" + str(os.environ.get('VOLUME_BACKUP_SCHEDULE', '0 0 * * *')),
        "--set", f"backup.schedule[0].keep=5",
        "--set", f"backup.schedule[1].name=s3-backup",
        "--set", f"backup.schedule[1].storageName=ceph-s3-us-west",
        "--set", f"backup.schedule[1].schedule=" + str(os.environ.get('S3_BACKUP_SCHEDULE', '0 0 * * 0')),
        "--set", f"backup.schedule[1].keep=5",
        "--create-namespace",
        "--values", "values.yaml"
    ])


def get_values(release, namespace):
    values = subprocess.run(["helm", "get", "values",  release, "-n", namespace, "--all", "-o", "yaml"], capture_output=True, text=True)
    values_file_name = release + '-' + namespace + '.yaml'
    with open(values_file_name, 'w') as file:
        file.write(values.stdout)

def main():
    add_helm_repo("percona", "https://percona.github.io/percona-helm-charts/")
    install_percona("percona/pxc-db", "1.14.0")
    release = os.environ.get('RELEASE_NAME')
    namespace = os.environ.get('NAMESPACE')
    get_values(release,namespace)


if __name__ == '__main__':
    main()
