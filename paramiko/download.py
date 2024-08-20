import paramiko
import os

# 设置远程服务器的IP地址、用户名和密码
hostname = "10.7.71.112"
username = "1"
password = "1"

# 创建一个SSH客户端连接
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

# 远程服务器上的文件夹路径
remote_folder = "/path/to/remote/folder"

# 本地文件夹路径
local_folder = "C:/Users/xx/Desktop/"

# 使用sftp客户端连接到远程服务器
sftp = ssh.open_sftp()

# 下载远程文件夹到本地
def download_folder(remote_folder, local_folder):
    for item in sftp.listdir(remote_folder):
        remote_item = os.path.join(remote_folder, item)
        local_item = os.path.join(local_folder, item)
        if sftp.isdir(remote_item):
            if not os.path.exists(local_item):
                os.makedirs(local_item)
            download_folder(remote_item, local_item)
        else:
            sftp.get(remote_item, local_item)


download_folder(remote_folder, local_folder)

# 关闭连接
sftp.close()
ssh.close()
