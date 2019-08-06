#! /usr/bin/env python
import scapy.all as scapy
import argparse 
import urllib.request as urllib2
import json
import codecs
from threading import Thread
def getargs ():
        parser=argparse.ArgumentParser()
        parser.add_argument("--target","-t",dest="target",help="Specify your target range")
        opt=parser.parse_args()
        if not opt.target :
                parser.error("[-] Please Specify a target !")
        else :
                return opt        
def getmacvend (mac) :
        url = "http://macvendors.co/api/"

        request = urllib2.Request(url+mac, headers={'User-Agent' : "API Browser"}) 
        response = urllib2.urlopen( request )
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(response))
        return obj['result']['company']
# Or Simply Arping can handle all of that but doing things from scratch is better :p
def scan(ip) :
    arp_req=scapy.ARP(pdst=ip)
    ether_broa=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broa=ether_broa/arp_req 
    answered = scapy.srp(arp_broa,timeout=5,verbose=False)[0]
    dest_list=[]
    for el in answered :
        dest_dict={"ip":el[1].psrc,"mac":el[1].hwsrc,"dev":getmacvend(el[1].hwsrc)}    
        dest_list.append(dest_dict)
    return dest_list

def print_res(result_list) :
        print("[+] Finished . \n\nIP\t\t\t Mac\t\t\tVendor\n--------------------------------------------------------------")
        for des in result_list :
                if len(des["dev"]) > 28 :
                        print(des["ip"]+"\t\t"+des["mac"]+"\t"+des["dev"][:28]+"-\n\t\t\t\t\t\t"+des["dev"][28:])        
                else :
                        print(des["ip"]+"\t\t"+des["mac"]+"\t"+des["dev"])



opt=getargs()
if opt is not None :
        try :
                print("[+] Scanning your Target ..")
                client_list=scan(opt.target)
                print_res(client_list)
        except :
                subprocess.call("clear")
                print("[-] An unexpected error has occured ! ")        
#See Yaa
