#!/bin/bash

setWlanIP=$(sed -n "1,1p" ip.conf)
echo Set wlan0 IP:$'\t'$setWlanIP

setEthIP=$(sed -n "2,2p" ip.conf)
echo Set eth0 IP:$'\t'$setEthIP

wlan0=$(ifconfig  wlan0 | head -n2 | grep inet | awk '{print$2}')
echo Current wlan0 IP:$'\t'$wlan0

eth0=$(ifconfig  eth0 | head -n2 | grep inet | awk '{print$2}')
echo Current eth0 IP:$'\t'$eth0

if [ ${#eth0} -eq 0 ]
then
    echo "[ERR!]No eth0 connection checked"
    exit 1
else
    if [ $eth0 = $setEthIP ]
    then
        echo "Correct eth0 connection checked"
    else
        echo "[ERR!]Wrong eth0 connection checked"
        exit 2
    fi
fi

if [ ${#wlan0} -eq 0 ]
then
    echo "[ERR!]No wlan0 connection checked"
    exit 3
else
    if [ $wlan0 = $setWlanIP ]
    then
        echo "Correct wlan0 connection checked"
    else
        echo "[ALM!]Different wlan0 connection checked"
    fi
fi

eth0Array=($(echo "$eth0" | tr '.' '\n'))
wlan0Array=($(echo "$wlan0" | tr '.' '\n'))

#echo "ip route add ${eth0Array[0]}.${eth0Array[1]}.${eth0Array[2]}.0/24 dev eth0 src $eth0 table 200"
#echo "ip route add default via ${eth0Array[0]}.${eth0Array[1]}.${eth0Array[2]}.1 dev eth0 table 200"
#echo "ip rule add from $eth0 lookup 200"
#echo "ip route add ${wlan0Array[0]}.${wlan0Array[1]}.${wlan0Array[2]}.0/24 dev wlan0 src $wlan0 table 100"
#echo "ip route add default via ${wlan0Array[0]}.${wlan0Array[1]}.${wlan0Array[2]}.1 dev wlan0 table 100"
#echo "ip rule add from $wlan0 lookup 100"

cmd1="ip route add ${eth0Array[0]}.${eth0Array[1]}.${eth0Array[2]}.0/24 dev eth0 src $eth0 table 200"
cmd2="ip route add default via ${eth0Array[0]}.${eth0Array[1]}.${eth0Array[2]}.1 dev eth0 table 200"
cmd3="ip rule add from $eth0 lookup 200"
cmd4="ip route add ${wlan0Array[0]}.${wlan0Array[1]}.${wlan0Array[2]}.0/24 dev wlan0 src $wlan0 table 100"
cmd5="ip route add default via ${wlan0Array[0]}.${wlan0Array[1]}.${wlan0Array[2]}.1 dev wlan0 table 100"
cmd6="ip rule add from $wlan0 lookup 100"

$cmd1
$cmd2
$cmd3
$cmd4
$cmd5
$cmd6

echo "Update route table sucessfully."
