#!/bin/sh

host_from="$1"
host_to="$2"

for n in `seq "$host_from" "$host_to"`; do
  echo "[+] using gateway 192.168.1.$n"
  sudo ip route add 192.168.3.0/24 via "192.168.1.$n"
  timeout 5s python client.py 192.168.3.2 
  sudo ip route del 192.168.3.0/24 via "192.168.1.$n"
done
