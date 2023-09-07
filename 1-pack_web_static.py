#!/usr/bin/python3
"""Archives web_static folder for web app deployment with Fabric"""
import os
from datetime import datetime
from fabric.api import local


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
