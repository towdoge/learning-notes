import os
import stat
import paramiko


def mkdir_p(sftp, remote_directory):
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == "/":
        # absolute path so change directory to root
        sftp.chdir("/")
        return
    if remote_directory == "":
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory)  # sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip("/"))
        print("make parent dir {}".format(dirname))
        mkdir_p(sftp, dirname)  # make parent directories
        sftp.mkdir(basename)  # sub-directory missing, so created it
        sftp.chdir(basename)
        return True


def copy_folder_by_sftp(
    hostname, username, password, local, remote, direction="local_to_remote"
):
    """
    copy folder by sftp, direction can be 'local_to_remote' or 'remote_to_local'
    :param hostname: str, hostname of the remote server
    :param username: str, username for authentication
    :param password: str, password for authentication
    :param local: str, local or remote source folder path
    :param remote: str, local or remote target folder path
    :param direction: str, 'local_to_remote' or 'remote_to_local'
    :return:
    """
    print("copy file {} {} {}".format(direction, local, remote))

    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        if direction == "local_to_remote":
            mkdir_p(sftp, remote)
            _copy_folder_by_recursion(sftp, local, remote, direction=direction)
            sftp.close()
        elif direction == "remote_to_local":
            os.makedirs(local, exist_ok=True)
            _copy_folder_by_recursion(sftp, local, remote, direction=direction)
            sftp.close()
            print("SCP transfer completed")
        else:
            raise ValueError(
                "Invalid direction. Please choose 'local_to_remote' or 'remote_to_local'."
            )
    finally:
        # Always close the transport when done
        transport.close()
        print("copy file over")


def _copy_folder_by_recursion(
    sftp, local_path, remote_path, direction="local_to_remote"
):
    """
    copy folder by recursion with sftp
    :param sftp: paramiko.SFTPClient instance
    :param local_path: str, local source folder path
    :param remote_path: str, remote target folder path
    :return:
    """
    if direction == "local_to_remote":
        for item in os.listdir(local_path):
            local_item_path = os.path.join(local_path, item)
            remote_item_path = os.path.join(remote_path, item)
            if os.path.isdir(local_item_path):
                mkdir_p(sftp, remote_item_path)
                _copy_folder_by_recursion(
                    sftp, local_item_path, remote_item_path, direction
                )
            else:
                sftp.put(local_item_path, remote_item_path)
    else:
        for item in sftp.listdir(remote_path):
            local_item_path = os.path.join(local_path, item)
            remote_item_path = os.path.join(remote_path, item)
            print(local_item_path, remote_item_path)
            remote_stats = sftp.lstat(remote_item_path)
            if stat.S_ISDIR(remote_stats.st_mode):
                os.makedirs(local_item_path, exist_ok=True)
                _copy_folder_by_recursion(
                    sftp, local_item_path, remote_item_path, direction
                )
            else:
                sftp.get(remote_item_path, local_item_path)

