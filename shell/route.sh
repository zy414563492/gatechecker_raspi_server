ip route add 192.168.1.0/24 dev eth0 src 192.168.1.8 table 200
ip route add default via 192.168.1.1 dev eth0 table 200
ip rule add from 192.168.1.8 lookup 200

ip route add 192.168.1.0/24 dev wlan0 src 192.168.1.180 table 100
ip route add default via 192.168.1.1 dev wlan0 table 100
ip rule add from 192.168.1.180 lookup 100
