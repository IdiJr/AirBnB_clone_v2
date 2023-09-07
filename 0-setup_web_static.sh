#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static and exits successfully

# Updates packages and Install nginx server if it is not available
sudo apt-get update
sudo apt-get -y install nginx

# Creates the folders
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# Inserts a pseudo html file into the test folder
echo -e "<html>\n    <head>\n    </head>\n    <body>\n        HolbertonSchool\n    </body>\n</html>" | sudo tee -a /data/web_static/releases/test/index.html

# Creates a symbolic link between /data/web_static/current & /data/web_static/releases/test/
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Changes ownership of the /data/ folder to ubuntu
chown -R ubuntu:ubuntu /data/

# Updates nginx configuration to serve content of /data/web_static/current/
sed -i '29a \ \tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# restarts nginx server
sudo service nginx restart
