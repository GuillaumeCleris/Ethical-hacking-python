#!/usr/bin/env python
import subprocess  # module to execute commands
import optparse  # module to use arguments
import re  # module to use regex


# @ Requires nothing
# @ ensures get command-line arguments (interface and mac address)
# @ raises nothing
def get_arguments():
	# creation of the parser
	parser = optparse.OptionParser()

	# define the structure of the first argument
	parser.add_option("-i", "--interface", dest="interface", help="Interface to change its Mac address")

	# define the structure of the second argument
	parser.add_option("-m", "--mac", dest="new_mac", help="New Mac address")
	# get arguments :
	# arguments.interface = "-i" or "--interface"
	# arguments.new_mac = "-m" or "--mac"
	# options.interface = the input of interface
	# options.new_mac = the input of mac
	(options, arguments) = parser.parse_args()

	# test if an input is missing
	if not options.interface:
		parser.error("[-] Please specify an interface, use - -help for more info ")
	elif not options.new_mac:
		parser.error("[-] Please specify an interface, use - -help for more info ")
	return options


# @ Requires a name of an interface, a mac address
# @ ensures change the mac address for interface to new_mac
# @ raises nothing
def change_mac(interface, new_mac):
	print("[+] Changing Mac address for " + interface + "to " + new_mac)
	# subprocess.call("ifconfig " + interface + " down",shell=True)) does not check what is sending
	subprocess.call(["ifconfig", interface, "down"])  # Stop the interface
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])  # modify the interface
	subprocess.call(["ifconfig", interface, "up"])  # open the interface


# @ Requires the name of an interface on the network
# @ ensures return the mac address of an interface in ifconfig or print "Could not read Mac address"
# @ raises nothing
def get_current_mac(interface):

	# execute ifconfig interface
	ifconfig_result = subprocess.check_output(["ifconfig", interface])

	# extracting mac address from ifconfig interface with a regex
	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

	# lo is an interface without mac address written in ifconfig.
	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Could not read Mac address.")


# get the command-line arguments
options = get_arguments()
# get the current mac address of the interface
current_mac = get_current_mac(options.interface)
# str casting to avoid the lo case (get_current_mac can return a string or print something)
print("Current Mac = " + str(current_mac))

# change mac address of the interface
change_mac(options.interface, options.new_mac)

# get the current mac address of the interface
current_max = get_current_mac(options.interface)

# check if mac address in ifconfig is what the user requested
if current_max == options.new_mac:
	print("[+] Mac address was successfully changed to " + current_mac)
else:
	print("[-] Mac address did not get changed.")
