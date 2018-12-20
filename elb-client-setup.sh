#!/bin/bash
mode=$1

yum install python2 vim -y
lb_ip="192.168.1.17"
if [ -z $mode ]; then
echo "Usage: `basaname $0` [scon|lcon|sudp|ludp]"
exit 1
fi

if [ $mode == "scon" ]; then
sh curl.sh $lb_ip 80
elif [ $mode == "lcon" ]; then
nohup python sock_connect.py $lb_ip 8080 &
sleep 2
tailf $lb_ip\:8080.log
elif [ $mode == "sudp" ]; then
python udp_client.py 1000 $lb_ip  5001 
elif [ $mode == "ludp" ]; then
python udp_client.py 2000 $lb_ip  5001 
fi


