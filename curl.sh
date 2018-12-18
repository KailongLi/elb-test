#!/bin/sh

host=$1
port=$2

if [ -z $host ]; then
echo "Usage: `basename $0` [HOST]"
exit 1
fi
log_name=$host"_"$port"_curl.log"

while :; do
result=`curl --connect-timeout 5 -m 1 "http://$1:$2"`
if [ $? -gt 0 ]; then
echo -e "`date +'%Y/%m/%d %H:%M:%S'` - host $host is \033[0;31mdown\033[0m"| tee -a $log_name
sleep 1
continue
else
echo -e "`date +'%Y/%m/%d %H:%M:%S'` - host $host is \033[0;32mok\033[0m"| tee -a $log_name
fi
sleep 1
done


