#!/bin/sh
# Sets up this machine for its part in the lab, then keeps it running.
# LAB_FAULT (gateway, dns, firewall or server) plants a fault for Module 6.
set -e
me=$(hostname)
fault=${LAB_FAULT:-}

# Docker gives every container its own address: swap it for the lab's.
ip addr flush dev eth0

gateway=
case "$me" in
  pc1)    ip addr add 192.168.10.21/24 dev eth0;  gateway=192.168.10.254 ;;
  pc2)    ip addr add 192.168.10.22/24 dev eth0;  gateway=192.168.10.254 ;;
  router) ip addr add 192.168.10.254/24 dev eth0
          ip addr add 10.0.20.254/24 dev eth0 ;;
  dns)    ip addr add 10.0.20.53/24 dev eth0;     gateway=10.0.20.254 ;;
  web)    ip addr add 10.0.20.80/24 dev eth0;     gateway=10.0.20.254 ;;
esac

dns_server=10.0.20.53
if [ "$me" = pc1 ] && [ "$fault" = gateway ]; then gateway=192.168.10.1; fi
if [ "$me" = pc1 ] && [ "$fault" = dns ]; then dns_server=10.0.20.35; fi

if [ -n "$gateway" ]; then ip route add default via "$gateway" dev eth0; fi
printf 'nameserver %s\nsearch cafe.lan\n' "$dns_server" > /etc/resolv.conf
printf '127.0.0.1\tlocalhost\n' > /etc/hosts

case "$me" in
  router)
    if [ "$fault" = firewall ]; then iptables -A FORWARD -p tcp --dport 80 -j DROP; fi ;;
  dns)
    exec dnsmasq --keep-in-foreground ;;
  web)
    if [ "$fault" != server ]; then httpd -p 80 -h /www; fi ;;
esac

exec sleep infinity
