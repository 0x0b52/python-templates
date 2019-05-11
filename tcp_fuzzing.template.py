#!/usr/bin/env python3
# coding=utf-8
#
# Template for fuzzing over TCP
#
# target: {OS, SERVICE NAME, IP, PORT}
#
# {SERVICE} Protocol Specifications:
#
#       {LINK TO RFC}
#        n bytes       string?    n bytes <...>
#       ----------------------------------------
#       | {meaning} | {meaning} | <...>
#       ----------------------------------------
#               {PACKET DESCRIPTION}
#
# aim: fuzz dynamic parameter, crash the service
# 
# Interaction:
#   {WRITE A DESCRIPTION ON HOW TO INTERACT WITH THE SERVICE}
#
# Example:
#   {EXAMPLE OF THE INTERACTION (WIRESHARK|NC|SH)}
#   
# author: {author}
#
# date: {date}
#
# pseudocode:
#   1) check if port is open
#   2) connect
#   3) send GET request
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
app_name = ""       # TODO: CHANGE HERE
junk = "\x44" * 10  # how many bytes to send?
target = ""         # TODO: CHANGE HERE
port = 0            # TODO: CHANGE HERE 
mmin = 40           # min number of input chars
mmax = 6000         # max number of input chars
sleep_time = 1      # Sleep for half a second to follow the fuzz


# functions
def print_recv(data):
    """
    Print any data if received.
    """
    if(len(data) > 0):
        print("[o] Received: " + data)


def check_port_tcp():
    """
    Safety check.
    """
    global target
    global port
    global app_name
    print('[!] Checking if ' + app_name + ' is online (' + target + ':' + str(port) + ')')
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(2)
        conn.connect((target,port))
        return True
    except Exception as e:
        print("[-] Error: ",end="")
        print(e)
        return False
    finally:
        conn.close()


def buff_builder(rdBuff):
    """
    Building HTTP headers
    """
    # EXAMPLE # TODO: CHANGE HERE
    # NOTE: Fuzzing HOST parameter

#    HTTP EXAMPLE: 
#    GET /example.html HTTP/1.1
#    Host: 127.0.0.1:6677
#    User-Agent: Mozilla/5.0 (X11; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1
#    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
#    Accept-Language: en-us,en;q=0.5
#    Accept-Encoding: gzip, deflate
#    Connection: keep-alive
#    Pragma: no-cache
#    Cache-Control: no-cache

    # string builder
    sb = ""
    sb = sb + 'GET /example HTTP/1.1\r\n'
    sb = sb + 'Host: ' + rdBuff + '\r\n'
    sb = sb + 'User-Agent: Mozilla/5.0 (X11; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1\r\n'
    sb = sb + 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' + '\r\n'
    sb = sb + 'Accept-Language: en-us,en;q=0.5'+ '\r\n'
    sb = sb + 'Accept-Encoding: gzip, deflate'+ '\r\n'
    sb = sb + 'Connection: keep-alive'+ '\r\n'
    sb = sb + 'Pragma: no-cache'+ '\r\n'
    sb = sb + 'Cache-Control: no-cache'+ '\r\n'
    sb = sb + '\r\n'

    return sb


def fizz():
    """
    Idea: Find the length of buffer to overwrite EIP.
    Make sure that server is happy with the input (e.g. reply 200:OK).
    """
    # value found: ???? bytes

    global app_name
    print("[*] Getting ready to fuzz " + app_name)
    global junk
    global mmin
    global mmax
    global sleep_time

    # remember: TCP
    try:
        while(True):
            # check if port is open:
            check = check_port_tcp()
            if(check == False):
                break
            print("[+] Service is online, start fuzzing")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
            print("[*] Connecting..")
            sock.connect((target,port))

            # HERE FUZZING STARTS
            # generate random string as per modiifer
            rd = ''.join([random.choice(string.ascii_letters)\
                for n in range(random.randrange(mmin,mmax))])
            print("[!] Sending %d bytes" % (len(rd)))

            sock.sendall((buff_builder(rd)).encode())

            print("[!] Closing connection")
            sock.close()
            time.sleep(sleep_time)
            sock.close() # for safety
    except Exception as e:
        print("[-] Error connecting to %s:%d"%(target,port))
        print(e)
        sock.close() # for safety


# main
def main():
    """
    Main method.
    """
    print("[+] sbot's fuzzer started")
    global app_name
    global target
    global port
    if (len(app_name) < 1 or len(target) < 1 or port == 0):
        sys.stderr.buffer.write(b"[-] Cannot use default template. Terminating!\n")
        sys.exit(0)
    fizz()


# run
if(__name__ == '__main__'):
    main()
    print("[*] done.. -__-")
