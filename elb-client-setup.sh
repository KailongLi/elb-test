#!/bin/bash
mode=$1

yum install python2 vim -y
lb_ip="114.116.108.69"
if [ -z $mode ]; then
echo "Usage: `basaname $0` [scon|lcon|sudp|ludp]"
exit 1
fi

if [ $mode -eq "scon" ]; then

elseif 
python udp_client.py 1000 $lb_ip  5001 


