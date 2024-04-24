import os

import paramiko


def scp_file(analysis_id):
    """
    copy all input file into one computer for debug
    :return:
    """

    source_hostname = "172.24.19.11"
    source_username = "root"
    source_password = "atl123456"

    local_folder = "/opt/workdir/atl/{}".format(analysis_id)
    remote_folder = "/opt/workdir/bak/{}".format(analysis_id)
    print("copy file from {} to {}".format(local_folder, remote_folder))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(source_hostname, username=source_username, password=source_password)

    sftp = client.open_sftp()
    try:
        sftp.stat(remote_folder)
    except FileNotFoundError:
        sftp.mkdir(remote_folder)

    # 递归所有子文件夹
    def copy_folder(local_folder, remote_folder):
        for item in os.listdir(local_folder):
            local_item_path = os.path.join(local_folder, item)
            remote_item_path = os.path.join(remote_folder, item)
            if os.path.isdir(local_item_path):
                try:
                    sftp.mkdir(remote_item_path)
                except:
                    pass
                copy_folder(local_item_path, remote_item_path)
            else:
                sftp.put(local_item_path, remote_item_path)

    copy_folder(local_folder, remote_folder)
    print("copy file over")
    sftp.close()
    client.close()
