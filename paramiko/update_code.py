import paramiko
from numpy import any
import sys
import subprocess

# 定义服务器信息
pro_servers = [
    {
        "ip": "172.23.8.130",
        "port": 22,
        "username": "root",
        "password": "Atl-2019",
        "workdir": "/opt/workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    },
    {
        "ip": "172.23.8.131",
        "port": 22,
        "username": "root",
        "password": "Atl-2019",
        "workdir": "/opt/workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    }, {
        "ip": "172.23.8.197",
        "port": 22,
        "username": "root",
        "password": "atl123456",
        "workdir": "/opt/produce_workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    },{
        "ip": "172.23.8.198",
        "port": 22,
        "username": "root",
        "password": "atl123456",
        "workdir": "/opt/workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    }, {
        "ip": "172.23.8.199",
        "port": 22,
        "username": "root",
        "password": "atl123456",
        "workdir": "/opt/workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    }, {
        "ip": "172.23.8.200",
        "port": 22,
        "username": "root",
        "password": "atl123456",
        "workdir": "/opt/workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    }, {
        "ip": "10.17.170.82",
        "port": 22,
        "username": "root",
        "password": "Atl-2019",
        "workdir": "/opt/workdir/server",
    },
]
uat_servers = [
    {
        "ip": "172.23.8.196",
        "port": 22,
        "username": "root",
        "password": "atl123456",
        "workdir": "/opt/workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    },
    {
        "ip": "172.23.8.197",
        "port": 22,
        "username": "root",
        "password": "atl123456",
        "workdir": "/opt/workdir/server",
        "jump_ip": "172.23.11.206",
        "jump_port": 22,
        "jump_username": "root",
        "jump_password": "Atl-2019",
    },
]

def ssh_connect(
    ip,
    port,
    username,
    password,
    jump_ip=None,
    jump_port=None,
    jump_username=None,
    jump_password=None,
    local_ip="10.17.170.82",
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


def main(env="pro", branch=""):
    servers = pro_servers if env == "pro" else uat_servers
    # 工作目录和命令

    for server in servers:
        workdir = server.get("workdir", "/opt/workdir/server")
        git_checkout = f"cd {workdir} && git checkout {branch}"
        get_uwsgi_pid1 = "cat /opt/workdir/server/uwsgi.pid"
        get_uwsgi_pid2 = "cat /opt/produce_workdir/server/uwsgi.pid"
        git_fetch = f"cd {workdir} && git fetch"
        git_stash = f"cd {workdir} && git stash"
        git_stash_pop = f"cd {workdir} && git stash pop"
        git_pull = f"cd {workdir} && git pull"
        git_rev = f"cd {workdir} && git rev-parse HEAD"
        check_uwsgi_command = "ps -ef | grep 'uwsgi' | grep -v grep | awk '{print}'"
        uwsgi_reload_command = f"uwsgi --reload {workdir}/uwsgi.pid"
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
            # there will be more than one uwsgi server
            uwsgi_pids = []
            output, error = execute_command(ssh, get_uwsgi_pid1)
            uwsgi_pid = output.split("\n")[0]
            uwsgi_pids.append(uwsgi_pid)
            output, error = execute_command(ssh, get_uwsgi_pid2)
            uwsgi_pid = output.split("\n")[0]
            uwsgi_pids.append(uwsgi_pid)

            # 执行git fetch 和 git pull
            output, error = execute_command(ssh, git_fetch)

            if branch:
                output, error = execute_command(ssh, git_checkout)
                print("切换到分支: {}".format(branch))

            output, error = execute_command(ssh, git_pull)
            if error:
                print(f"Git pull 操作失败: {error}")
                continue

            output, error = execute_command(ssh, git_rev)
            print("当前commit id {}".format(str(output).split('\n', maxsplit=1)[0]))

            # 检查uwsgi是否在运行算法
            output, error = execute_command(ssh, check_uwsgi_command)
            if error:
                print("查询失败，尝试重新加载...")
                continue
            existed = False
            list_uwsgi = output.split("\n")

            for k in list_uwsgi:
                if k == "":
                    continue
                # if it is defunct process
                elif any(["defunct" in id for id in k.split(" ")]):
                    print("defunct pid {}".format(k))
                    continue
                # if it is server process
                elif any([id in uwsgi_pids for id in k.split(" ")]):
                    continue
                else:
                    print("processing pid {}".format(k))
                    existed = True
                    break
            if existed:
                print("uwsgi正在运行算法，稍等...\n")
                continue
            else:
                output, error = execute_command(ssh, uwsgi_reload_command)
                if error:
                    print("uwsgi更新失败...\n")
                    continue
                else:
                    print("uwsgi更新成功...\n")
        finally:
            if ssh:
                ssh.close()


if __name__ == "__main__":
    env = "pro" if len(sys.argv) <= 1 else sys.argv[1]
    branch = "" if len(sys.argv) <= 2 else sys.argv[2]
    main(env, branch)
