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
