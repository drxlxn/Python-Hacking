#!/usr/bin/env python

import scapy.all as scapy  # importing modules
import argparse
import sys


def get_argument():  # fetch arguments for target IP
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range")  # arguments defined
    options = parser.parse_args()
    if len(sys.argv) <= 1:
        print('Error: No arguments')
        print('Type -h for help')
        sys.exit(1)
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  # my IP address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # broadcast mac address
    arp_request_broadcast = broadcast / arp_request  # combines two variables into one
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]  # catches results in variable

    clients_list = []  # empty list
    for element in answered_list:
        clients_dict = {"IP": element[1].psrc, "MAC": element[1].hwsrc}
        clients_list.append(clients_dict)  # adds value, directory created above, into the empty list
    return clients_list


def print_result(results_list):
    print("IP\t\t\t MAC Address\n------------------------------------------")
    for client in results_list:
        print(client["IP"] + "\t\t" + client["MAC"])  # display the values of the directory/list


options = get_argument()
scan_result = scan(options.target)
print_result(scan_result)
