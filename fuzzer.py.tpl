#!/usr/bin/env python3
# coding=utf-8
#
# <short_description>
#
# target: <[software|IP|port|OS]>
#
# <target_description>
#
# <communication_protocol|RFC_standard>
#
# <interaction_example:wireshark|nc]>
#
# author: <[nick|name]>
#
# date: dd/mm/yyyy 
#
# pseudocode:
#   1) connect
#   2) send command
#   3) receive
#   4) fuzz until crashed
#   5) close connection
#
# imports
import os
import sys
import socket
import time
import random
# import argparse # TODO: Update template to accomodate


# vars
app_name = "<change_me>"
junk = "\x41" * 10    # how many bytes to send?
target = "IP_ADDRESS" # TODO: Change
port = 1337           # TODO: Change
modifier = 1000       # initial state
sleep_time = 0.5      # Sleep for half a second to follow the fuzz


# functions
def print_recv(data):
  if(len(data) > 0):
        print("[o] Received: " + data)

      
def fizz():
  """
  Idea: Find the length of buffer to overwrite EIP.
  """
  # value found: ???? bytes # TODO: Write here once done
  global app_name
  print("[*] Getting ready to fuzz " + app_name)
  global junk
  global modifier
  global sleep_time
  
  try:
    while(True):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
      # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
      print("[*] Connecting..")
      sock.connect((target,port))
      data = sock.recv(1024).decode()
      print_recv(data)
        
      # HERE FUZZING STARTS
      # TODO: required? Any data to be sent before getting to our FUZZed parameter
      # TODO: [delete|uncomment] as required
      # sock.send(('<PARAM> <STRING>' + '\r\n').encode()) 
      # data = sock.recv(1024).decode()
      # print_recv(data)
      print("[!] Sending %d bytes" % (len(junk)))
      sock.send(('<PARAM>' + junk + '\r\n').encode()) # TODO: Edit the parameter you are fuzzing
      data = sock.recv(1024).decode()
      print_recv(data)
      sock.close()
      print("[!] Connection closed")
      modifier = modifier + 100 # TODO: Change modifier as required
      time.sleep(sleep_time)
    except Exception as e:
      print("[-] Error connecting to %s:%d"%(target,port))
      print e
    finally:
      #sock.send(("EXIT\r\n").encode()) # TODO: [delete|uncomment]
      sock.close() # for safety


# main
def main():
  print("[+] sbot's fuzzer started")
  fizz()
  
  
# run
if(__name__ == '__main__'):
  main()
  print("[*] done.. -__-")
