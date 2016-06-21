# Example that performs port scanning

# Import scapy library and all its dependencies
from scapy.all import *

# Craft the scanner by sending a TCP/IP packet with
# the TCP flag set to SYN to every port in the range
# 1-1024 (it will take a while to scan)

res, unans = sr(IP(dst='192.168.1.114')/TCP(flags='S', dport=(1, 1024)))

# Check the output
res.summary()






