#!/usr/bin/env python3                   
# coding=utf-8
#
# Template for fuzzing over UDP protocol
#
# Target: {OS, SERVICE NAME, IP, PORT}
#
# {SERVICE} Protocol Specifications:
#
#       {LINK TO RFC}
#        n bytes    string?     n bytes <...>
#       -------------------------------------------------
#       | {meaning} |  {meaining}  | <...>
#       -------------------------------------------------
#               {PACKET DESCRIPTION}
#
# Aim: fuzz the input ({string|parameter|value})
#
# Interaction:
#       {WRITE DESCRIPTION ON HOW TO INTERACT WITH THE SERVICE}
#
# Example:
#   {EXAMPLE OF THE INTERACTION (WIRESHARK|NC|SH)}
#
# Author: {author}
#
# Date: {date}
#
# pseudocode:
#   1) check if port is open
#   2) connect
#   3) send command
#   4) receive
#   5) fuzz until crashed
#   6) close connection
#
# imports
import os
import sys
import socket
import time
import random
import string


# vars
app_name = ""         # TODO: CHANGE HERE
junk = "\x44" * 10    # how many bytes to send?
target = ""           # TODO: CHANGE HERE
port = 123            # TODO: CHANGE HERE
mmin = 400            # min number of input chars
mmax = 5000           # max number of input chars
sleep_time = 1       # Sleep for half a second to follow the fuzz


# functions
def print_recv(data):
    """
    Show the received data (if any)
    """
    if(len(data) > 0):
        print("[o] Received: " + data)


def check_port_udp():
    """
    Safety check.
    """
    global target
    global port
    global app_name
    print('[!] Checking if %s' %(app_name) + ' is online')
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c.settimeout(2)
        c.sendto("pidr".encode(),(target,port))
        data = c.recvfrom(1024)

        # DEBUG
        # print("Data:" + data.decode())

        if(len(data)>1):
            return True
        else:
    except Exception as e:
        print("[-] Error: ",end="")
        print(e)
        return False

    finally:
        c.close()


def fizz():
    """
    Discover the length of buffer to overwrite EIP.
    """
    # value found: ???? bytes

    global app_name
    print("[*] Getting ready to exploit " + app_name)
    global junk
    global mmin
    global mmax
    global sleep_time

    # remember: UDP
    try:
        while(True):
            # check if port is open:
            check = check_port_udp()
            if(check == False):
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            print("[*] Connecting..")

            # HERE FUZZING STARTS
            # generate random string as per modifier
            rd = ''.join([random.choice(string.ascii_letters)\
                for n in range(random.randrange(mmin,mmax))])
            print("[!] Sending %d bytes" % (len(rd)))
            sock.sendto(('\x00\x00' + rd).encode(),(target,port)) # TODO: CHANGE HERE TO FIT THE PROTO
            sock.close()
            print("[!] Closing connection")
            time.sleep(sleep_time)
            sock.close() # for safety
    except Exception as e:
        print("[-] Error connecting to %s:%d"%(target,port))
        print(e)
        sock.close() # for safety

        
# main
def main():
    print("[+] sbot's fuzzer started")
    fizz()


# run
if(__name__ == '__main__'):
    global app_name
    if (len(app_name) < 1):
        print("[!] You are using an empty template! Implement all the changes.")
        sys.exit(0)
    main()
    print("[*] done.. -__-")
