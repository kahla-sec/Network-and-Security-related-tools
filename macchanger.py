#!/usr/bin/env python
import subprocess
import optparse
import re

def getargs() :
    parser=optparse.OptionParser()
    parser.add_option('-i','--interface',dest='interface',help='Add your interface to chnage its mac address')
    parser.add_option('-m','--mac',dest='mac',help='The new Mac address')
    parser.add_option('-c','--check',dest='check',action='store_true', default=False,help='Print your current mac address')
    (options,args)=parser.parse_args()
    if options.check and options.interface:
        print('[+] Your current Mac address is: '+ currmac(options.interface))    
    elif not options.interface :
        parser.error("[-] Please specify an interface")
    elif not options.mac :
        parser.error("[-] Please specify an address mac")     
    else :
        return options


def changemac(interface,mac) :
    print('[+] Changing your mac address to '+ mac)
    subprocess.call(['ifconfig',interface,'down'])
    subprocess.call(['ifconfig',interface,'hw','ether',mac])
    subprocess.call(['ifconfig',interface,'up'])


def check(interface,mac):
    out=subprocess.check_output(['ifconfig',interface])
    var=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",out.decode('utf-8'))
    if var.group(0)==mac :
        print('[+] Mac Address Succesfully changed !')
    else :
        print('[-] Couldn\'t change mac address' )

def currmac(interface):
    out=subprocess.check_output(['ifconfig',interface])
    var=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",out.decode('utf-8'))
    return var.group(0)   


opt=getargs() 
if opt is not None :
    changemac(opt.interface,opt.mac)
    check(opt.interface,opt.mac)