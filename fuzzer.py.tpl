#!/usr/bin/env python3
# coding=utf-8
#
# <short_description>
#
# target: <[software|IP|port|]>
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
#   4) fuzz intil crashed
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



# functions
def fizz():
  """
  Idea: Find the length of buffer to overwrite EIP.
  """
  # value found: ???? bytes # TODO: Write here once done
  global app_name
  print("[*] Getting ready to fuzz " + app_name)
  global junk
  global modifier
  
  try:
    while(True):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
      # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
      print("[*] Connecting..")
      sock.connect((target,port))
      data = sock.recv(1024).decode()
      if(len(data) > 0):
        print("[o] Received: " + data)
        
      # HERE FUZZING STARTS &#x1f618;
      
