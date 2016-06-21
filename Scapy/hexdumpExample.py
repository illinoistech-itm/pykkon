# Example of the useful hexdump function

# Import scapy library and all its dependencies
from scapy.all import *

# Convert into a string
str(IP())

# Creating packet
a = Ether()/IP(dst="www.google.com")/TCP()/"GET /index/html HTTP/1.1"

# Call the hexdump() function that display the one or more packets
# in classic hexdump format
hexdump(a)
