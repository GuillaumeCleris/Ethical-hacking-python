#!/usr/bin/env python 


import scapy.all as scapy
import optparse


# @ Requires nothing
# @ ensures get command-line arguments (interface and mac address)
# @ raises nothing
def get_arguments():
	# creation of the parser
	parser = optparse.OptionParser()

	# define the structure of the first argument
	parser.add_option("-t", "--target", dest="target", help="Target IP")

	# get arguments :
	# arguments.target = "-t" or "--target"
	# options.target = the input of target
	(options, arguments) = parser.parse_args()

	# test if an input is missing
	return options


# @ Requires an ip address
# @ ensures return the list of devices on the network
# (each device is qualified by a dictionary including its ip and mac address)
# @ raises nothing
def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # ff obtenu grace à scapy.ls
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

	# create a list of dictionaries {"ip"= x, "mac"=y}
	clients_list = []
	for element in answered_list:
		# store the ip address and the mac address in a dictionary for each element of the list
		client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
		# add the dictionary in the list
		clients_list.append(client_dict)
	return clients_list


# @ Requires a list of dictionaries {"ip"=,"mac"=}
# @ ensures print a table with the ip and mac address of the devices on the network
# @ raises nothing
def print_result(results_list):
	print("IP\t\t\tMac Address\n--------------------------------------------")
	for client in results_list:
		print(client["ip"] + "\t\t" + client["mac"])


scan_result = scan("10.0.2.1/24")
print_result(scan_result)
