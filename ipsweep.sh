#!/bin/bash
if [ $(echo $1|sed "s/\./ /g"|wc -w) -ne 4 ]
then
printf "<Usage> : $0 192.168.1.1\n"
else

str=$(echo $1|cut -d "." -f 4) 
length=${#str}
raw_ip=$1
for i in `seq 1 $length`;do
raw_ip=$(echo $raw_ip|sed 's/.$//') 
done
printf "Got response from these IPs :\n"
for ip in `seq 0 254`;do
ping -c 1 $raw_ip$ip|grep "64 bytes"|cut -d " " -f 4|tr -d ":" &
done
fi
