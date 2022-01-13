#!/usr/bin/env python

import scapy.all as scapy  # module for arp spoofing attack


# @ Requires an ip address
# @ ensures print a table with the ip and mac address connected on the network
# @ raises nothing
def scan(ip):
	# arp request "who has 10.0.2.1/24?"
	arp_request = scapy.ARP(pdst=ip)

	# arp incomplete answer "he has 10.0.2.1"
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # ff obtenu grace à scapy.ls

	# combine two packets
	arp_request_broadcast = broadcast/arp_request

	# get the list of the answers
	# verbose=FALSE to delete the "finished" and "begin"
	# send response but not capture
	# it is a list of two value (first value is ip / second is mac address)
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
	# We add a header
	print("IP\t\t\tMac Address\n--------------------------------------------")

	# separate the answers to have a clean display
	for element in answered_list:
		print(element[1].prsc + "\t\t" + element[1].hwsrc)
		print("----------------------------------------")


# Network_scanner : Discover all devices on the network / display their ip address and their mac address
scan("10.0.2.1/24")
