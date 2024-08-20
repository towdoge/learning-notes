#! /usr/bin/python3
# -*- coding: UTF-8 -*-
"""
  作者: 小肥爬爬
  简书: https://www.jianshu.com/u/db796a501972
  gitee: https://gitee.com/xiaofeipapa/python-toolkit
  您可以自由转载此博客文章, 恳请保留原链接, 谢谢!
"""
from fabric import Connection


def run_shell(conn, cmd, hide=True, warn=True, encoding='utf-8'):
    """
    远程执行外部cmd小工具
    :param conn:
    :param cmd:
    :param hide:
    :param warn:
    :param encoding:
    :return:
    """
    result = conn.run(cmd, hide=hide, warn=warn, encoding=encoding)
    # err = result.stdout.stderr()
    # if err:
    #     raise Exception(err)
    print(result.stdout.strip())
    return result


def do_it():
    host = '10.7.71.112'
    user = 'xx'
    password = 'xx'

    # ssh 连接的正确姿势
    conn = Connection(host=host, user=user, connect_kwargs={'password': password})

    # 在远程机器运行命令(用run方法), 并获得返回结果
    # hide 表示隐藏远程机器在控制台的输出, 达到静默的效果
    # 默认 warn是False, 如果远程机器运行命令出错, 那么本地会抛出异常堆栈. 设为True 则不显示这堆栈.
    cmd = 'cd /root/atlAPS/testData/xn/0411/'
    result = run_shell(conn, cmd)
    cmd = 'pwd'
    result = run_shell(conn, cmd)
    _path = "/root/atlAPS/testData/xn/0411/"
    # cmd = 'nohup python {}{} {}'.format(_path, "run_daily.py", _path)
    result = run_shell(conn, cmd)
    # 连续执行程序
    with conn.cd(_path):
        result = run_shell(conn, cmd)
    result = run_shell(conn, cmd)
    # # 正常运行时, 信息在 stdout里
    # print('-------- 下面是 stdout 信息')
    # print(result.stdout.strip())
    #
    # # 出错时, 信息在 stderr 里
    # print('-------- 下面是 stderr 信息')
    # print(result.stderr.strip())


if __name__ == '__main__':
    do_it()
