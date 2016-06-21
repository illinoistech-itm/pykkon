# Import Scapy Library and all dependencies
from scapy.all import *

# Using the sr() method that returns a couple of
# packets, answers and unanswered packets. See also sr1()
# Important to notice that sr() and sr1() are layer 3
# methods.
output = sr(IP(dst='google.com')/ICMP())

# Shows the results
print '\n Output is:' + str(output)
result, unanswered = output
print '\n Result is:' + str(result)
