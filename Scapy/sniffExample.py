# Examples of the sniff() Method

# Import scapy and all its dependencies
from scapy.all import *

# Sniff using iface (interface) as parameter, count
# specifies how many packets it should sniff, if 
# left blank the value is infinite
p = sniff(iface='eth5', timeout=10, count=5)

# Sniff specifying filters
p = sniff(filter="tcp and (port 25 or port 110)")

# It's possible to use sniff with a customized
# callback function to every packet that matches
# the filter

def packet_callback(packet):
    print packet.show()

sniff(filter='icmp', iface='eth5', prn=packet_callback, count=1)

# To see the output in real time and dump the data into a file
# use the lambda function with summary and wrpcap method

p = sniff(filter='icmp', iface='eth5', timeout=10, count=5,
        lambda x:x.summary())
wrpcap('packets.pcap', p)


