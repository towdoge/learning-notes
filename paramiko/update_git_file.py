import os
import subprocess

# 设置要遍历的根目录
root_dir = 'D:\\git'

# 遍历根目录及其子目录
for dirpath, dirnames, filenames in os.walk(root_dir):
    # 检查当前目录是否是Git仓库（即是否存在.git目录）
    git_dir = os.path.join(dirpath, '.git')
    if os.path.isdir(git_dir):
        # 构造git pull命令
        git_pull_cmd = ['git', 'pull']
        # 执行git pull命令
        try:
            print(f"正在更新 {dirpath}")
            subprocess.run(git_pull_cmd, cwd=dirpath, check=True)
        except subprocess.CalledProcessError as e:
            print(f"更新 {dirpath} 失败: {e}")

print("所有git仓库已更新完毕。")