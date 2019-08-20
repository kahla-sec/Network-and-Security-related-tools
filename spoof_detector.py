#!/usr/bin/env python
import scapy.all as scapy 
import argparse

def getargs() :
    parser=argparse.ArgumentParser()
    parser.add_argument("--interface","-i",dest="interface",help="Specify your interface")
    opt=parser.parse_args()
    if not opt.interface :
        parser.error("[-] Please specify your interface")
    else :
        return opt    

def filter_packets(packet):
    try:
        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2 :
            if getmac(packet[scapy.ARP].psrc) != packet[scapy.ARP].hwsrc :
                print("[+] You are under attack !!")
    except IndexError:
        pass        


def getmac(ip) :
    arp_req=scapy.ARP(pdst=ip)
    ether=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast=ether/arp_req ;
    answered=scapy.srp(arp_broadcast,timeout=2,verbose=False)[0]
    return answered[0][1].hwsrc

def detect (interface) :
    scapy.sniff(iface=interface,store=False,prn=filter_packets)


opt=getargs()
detect(opt.interface)