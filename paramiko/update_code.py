import paramiko
from numpy import any
import sys
import subprocess

# 定义服务器信息
pro_servers = [
    {
        "ip": "1.1.1.1",
        "port": 22,
        "username": "root",
        "password": "root",
        "jump_ip": "1.1.1.2",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "root",
    },
    {"ip": "1.1.1.3", "port": 22, "username": "root", "password": "root"},
]
uat_servers = [
    {"ip": "1.1.1.4", "port": 22, "username": "root", "password": "root"},
]

# 工作目录和命令
workdir = "/opt/workdir/server"
get_uwsgi_pid = f"cat {workdir}/uwsgi.pid"
git_fetch = f"cd {workdir} && git fetch"
git_commands = f"cd {workdir} && git pull"
check_uwsgi_command = "ps -ef | grep 'uwsgi' | grep -v grep | awk '{print}'"
uwsgi_reload_command = f"uwsgi --reload {workdir}/uwsgi.pid"


def ssh_connect(
    ip,
    port,
    username,
    password,
    jump_ip=None,
    jump_port=None,
    jump_username=None,
    jump_password=None,
    local_ip="1.1.1.1",
):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if ip == local_ip:
        return None
    # 如果需要通过跳板机连接
    if jump_ip:
        # 首先连接到跳板机
        ssh.connect(jump_ip, jump_port, jump_username, jump_password)
        ssh_transport = ssh.get_transport()
        src_addr = (jump_ip, 22)
        dest_addr = (ip, 22)
        jumpbox_channel = ssh_transport.open_channel(
            kind="direct-tcpip",
            dest_addr=dest_addr,
            src_addr=src_addr,
        )
        print("连接上了跳板机 {}".format(jump_ip))
        # 去连接远端服务器
        target_ssh = paramiko.SSHClient()
        target_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        target_ssh.connect(
            hostname=ip,
            port=port,
            username=username,
            password=password,
            sock=jumpbox_channel,
        )
        print("连接上了ip {}".format(ip))
        return target_ssh
    else:
        ssh.connect(ip, port, username, password)

    return ssh


def execute_command(ssh=None, command=""):
    if ssh:
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()  # 等待命令执行完成
        return stdout.read().decode(), stderr.read().decode()
    else:
        try:
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr


def main(env="pro"):
    servers = pro_servers if env == "pro" else uat_servers
    for server in servers:
        print(f"正在处理服务器：{server['ip']}")
        ssh = ssh_connect(
            server["ip"],
            server.get("port"),
            server["username"],
            server["password"],
            server.get("jump_ip"),
            server.get("jump_port"),
            server.get("jump_username"),
            server.get("jump_password"),
        )
        try:
            output, error = execute_command(ssh, get_uwsgi_pid)
            uwsgi_pid = output.split("\n")[0]
            # 执行git fetch 和 git pull
            output, error = execute_command(ssh, git_fetch)
            # if error:
            # print(f"Git fetch 操作失败: {error}")
            # continue
            output, error = execute_command(ssh, git_commands)
            if error:
                print(f"Git pull 操作失败: {error}")
                continue

            # 检查uwsgi是否在运行算法
            output, error = execute_command(ssh, check_uwsgi_command)
            if error:
                print("查询失败，尝试重新加载...")
                continue
            flag = False
            list_uwsgi = output.split("\n")
            # print(list_uwsgi)
            for k in list_uwsgi:
                if k == "":
                    continue
                print("pid {}".format(k))
                if any(["defunct" in id for id in k.split(" ")]):
                    continue
                if any([id == uwsgi_pid for id in k.split(" ")]):
                    continue
                else:
                    flag = True
                    break
            if flag:
                print("uwsgi正在运行算法，稍等...")
                continue
            else:
                output, error = execute_command(ssh, uwsgi_reload_command)
                if error:
                    print("uwsgi更新失败...")
                    continue
                else:
                    print("uwsgi更新成功...")
        finally:
            if ssh:
                ssh.close()


if __name__ == "__main__":
    env = "pro" if len(sys.argv) <= 2 else sys.argv[2]
    main(env)
