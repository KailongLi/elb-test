#!/bin/bash
yum install python2 vim nginx -y
sed -i '/        listen       80 default_server;/a\        listen       8080 default_server;' /etc/nginx/nginx.conf
nginx
nohup python udp_server.py 1000 5001 &


