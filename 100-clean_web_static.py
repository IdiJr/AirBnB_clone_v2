#!/usr/bin/python3
"""Distributes an archive to webservers, with Fabric"""
from fabric.api import local
from fabric.api import env
from fabric.api import run
from fabric.api import put
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['54.87.171.60', '100.25.181.220']


def do_pack():
    """generates a .tgz tar gzipped archive from web_static folder"""
    pack_time = datetime.utcnow()
    zip_files = "web_static_{}{}{}{}{}{}.tgz".format(
        pack_time.year, pack_time.month, pack_time.day,
        pack_time.hour, pack_time.minute, pack_time.second
    )
    output = "versions/{}".format(zip_files)
    if not os.path.exists("versions"):
        os.makedirs("versions")
    zipped = local("tar -cvzf {} web_static".format(output))
    if zipped.succeeded:
        file_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, file_size))
        return output
    else:
        return None


def do_deploy(archive_path):
    """Distribute and deploy an archive to web servers
    Args: archive_path (str): path to archived web_static files
    """
    if not os.path.isfile(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False
    if run("sudo rm -rf {}".format(folder_path)).failed:
        return False
    if run("sudo mkdir -p {}".format(folder_path)).failed:
        return False
    if run("sudo tar -xzf /tmp/{} -C {}"
            .format(file_name, folder_path)).failed:
        return False
    if run("sudo rm /tmp/{}".format(file_name)).failed:
        return False
    if run("sudo mv {}web_static/* {}"
            .format(folder_path, folder_path)).failed:
        return False
    if run("sudo rm -rf {}web_static".format(folder_path)).failed:
        return False
    if run("sudo rm -rf /data/web_static/current").failed:
        return False
    if run("sudo ln -s {} /data/web_static/current"
            .format(folder_path)).failed:
        return False

    print("New version deployed!")
    return True


def deploy():
    """
    Create and distribute an archive to a web server.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """ Deletes out-of-date archives of the web_static files
    Args:
        number (Any): The number of archives to keep.
    """
    number = int(number)
    local("ls -d -1tr versions/* | tail -n +{} | \
            xargs -d '\n' rm -f --".format(2 if number < 1 else number + 1))
    run("ls -d -1tr /data/web_static/releases/* | tail -n +{} | \
            xargs -d '\n' rm -rf --".format(2 if number < 1 else number + 1))
