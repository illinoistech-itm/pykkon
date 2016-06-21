# Import scapy library and all dependencies
from scapy.all import *

# Create an instance of an IP header
ip = IP(src='192.168.1.114', dst='192.168.1.25')

# Define a SYN instance of the TCP header
SYN = TCP(sport=1024, dport=80, flags='S', seq=12345)

# Create the packet
packet = ip/SYN

# Send and Capture the server's response using sr1()
SYNACK = sr1(packet)

# Extract the server's TCP seq. number for the server using
# SYNACK.seq and incrementing it by 1
ack = SYNACK.seq + 1

print ' Sever response: \n' + ack

# Create new instance of the TCP header ACK, which now has
# the flag A (ACK value)
ACK = TCP(sport=1024, dport=80, flags='A', seq=123456, ack=ack)

# Send everything
send(ip/ACK)

# Create the segment with no TCP flags
PUSH = TCP(sport=1024, dport=80, flags='', seq=123456, ack=ack)

# Create Payload
data = "HELLO!!" 

# Send it
send(ip/PUSH/data)

# This code won't work because crafting TCP sessions with Scapy
# circumvents the native TCP/IP stack. Since the host is unaware
# that Scapy is sending packets, the native host would receive
# an unsolicited SYN/ACK that is not associated with any known
# open session/socket. This would result in the host reseting the
# connection when receiving the SYN/ACK. One way to circumvent this
# is to use the host's firewall with iptables to block the outbound
# resets. For example, to drop all outbound packets that are TCP
# and destined for IP 192.168.1.25 from 192.168.1.114 to destination
# port 80, examining the flag bits we can run:

#   sudo iptables -A OUTPUT -p tcp -d 192.168.1.25 -s 192.168.1.114
# --dport 80 --tcp-flags RST -j DROP

# This doesn't prevent the source host from generating a reset each
# time it receives a packet from the session, however it does block
# it from silencing the resets.

