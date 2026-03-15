#!/bin/bash
SUBNET='10.19.11.0/24'
USERS_SUBNET='10.19.11.128/25'
CHALLANGES_SUBNET='10.19.11.0/29'
OTHER_UTILS_SUBNET='10.19.11.8/29'
SKY_SEC_SUBNET='10.19.11.32/27'

iptables -F
iptables -X

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p udp --dport 51820 -j ACCEPT

iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A FORWARD -s $SKY_SEC_SUBNET -j ACCEPT
iptables -A FORWARD -s $OTHER_UTILS_SUBNET -d $USERS_SUBNET -j ACCEPT
iptables -A FORWARD -s $CHALLANGES_SUBNET -d $USERS_SUBNET -j ACCEPT
iptables -A FORWARD -s $USERS_SUBNET -d $USERS_SUBNET -j DROP

# Wireguard Logs
iptables -I FORWARD -i wg0 -j LOG --log-prefix 'tunnel wireguard iptables: ' --log-level 7
iptables -I FORWARD -o wg0 -j LOG --log-prefix 'tunnel wireguard iptables: ' --log-level 7
