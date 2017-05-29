#!/usr/bin/env python

from pytun import TunTapDevice
from scapy.all import *
import os
import pytun
import time

SERVER_IP = "128.199.177.106"

# Open tun0 device
tun = TunTapDevice("leamit0",pytun.IFF_TUN | pytun.IFF_NO_PI)
tun.addr = "10.10.0.2"
tun.dstaddr = SERVER_IP
tun.netmask = "255.255.255.0"
tun.mtu = 1500
tun.up()

while 1:
    packet = IP(src="128.199.177.106",dst="10.10.0.1")/ICMP()
    packet.show()
    tun.write(packet.build())
    time.sleep(4)
