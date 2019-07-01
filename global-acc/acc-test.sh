eip=139.159.150.214
proxy_ip=192.168.1.188
nginx_proxy_ip=192.168.1.165

for i in {1..1}
do
echo "=======$i round start======"
nohup tcpdump -i eth0 host $eip -nnev -w eip-https-${i}.pcap &
curl https://$eip:443 -k 1> /dev/null 2>/dev/null
killall tcpdump
sleep 1

nohup tcpdump -i eth0 host $eip -nnev -w eip-http-${i}.pcap &
curl http://$eip:80 -k 1> /dev/null 2>/dev/null
killall tcpdump
sleep 1

nohup tcpdump -i eth0 host $proxy_ip -nnev -w lvs-https-${i}.pcap &
curl https://$proxy_ip:8443 -k 1> /dev/null 2>/dev/null  
killall tcpdump
sleep 1

nohup tcpdump -i eth0 host $proxy_ip -nnev -w lvs-http-${i}.pcap &
curl https://$proxy_ip:8080 -k 1> /dev/null 2>/dev/null
killall tcpdump
sleep 1


nohup tcpdump -i eth0 host $nginx_proxy_ip -nnev -w nginx-https-$i-1st.pcap &
curl https://$nginx_proxy_ip:443/proxy -k 1> /dev/null 2>/dev/null
killall tcpdump
sleep 1

nohup tcpdump -i eth0 host $nginx_proxy_ip -nnev -w nginx-https-$i-2nd.pcap &
curl https://$nginx_proxy_ip:443/proxy  -k 1> /dev/null 2>/dev/null
killall tcpdump
sleep 1

nohup tcpdump -i eth0 host $nginx_proxy_ip -nnev -w nginx-http-$i-1st.pcap &
curl https://$nginx_proxy_ip:80/proxy  -k 1> /dev/null 2>/dev/null
killall tcpdump
sleep 1

nohup tcpdump -i eth0 host $nginx_proxy_ip -nnev -w nginx-http-$i-2nd.pcap &
curl https://$nginx_proxy_ip:80/proxy  -k 1> /dev/null 2>/dev/null
killall tcpdump
sleep 1
echo "=======$i round end======="

done


