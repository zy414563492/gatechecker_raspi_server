#!/bin/bash

setEthIP=$(sed -n "2,2p" ip.conf)
echo Set eth0 IP:$'\t'$setEthIP

eth0Array=($(echo "$setEthIP" | tr '.' '\n'))

modi1="static ip_address=${setEthIP}/24"
modi2="static routers=${eth0Array[0]}.${eth0Array[1]}.${eth0Array[2]}.1"
modi3="static domain_name_servers=${eth0Array[0]}.${eth0Array[1]}.${eth0Array[2]}.1"

sed -i "64c${modi1}" /etc/dhcpcd.conf
sed -i "65c${modi2}" /etc/dhcpcd.conf
sed -i "66c${modi3}" /etc/dhcpcd.conf

echo "Update eth0 IP sucessfully."
