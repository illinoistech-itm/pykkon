# Simple script that sends a ICMP Packet

# Import Scapy library and all its dependencies
from scapy.all import *

# Create a layer 3 packet with destination IP 192.168.1.114
# with message Hello Sniffer
packet = IP(dest="192.168.1.114")/ICMP()/"Hello Sniffer"

# Send that packet
send(packet)

# Show the packets details
packet.show()
