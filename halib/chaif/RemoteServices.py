#! /usr/bin/env python
#
<<<<<<< HEAD
# Copyright (c) 2009 Okoye Chuka D.<okoye9@gmail.com>
=======
# Copyright (c) 2009 Himanshu Chhetri <himanshuchhetri@gmail.com>
>>>>>>> himanshu-database/master
#                    All rights reserved.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
 
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import socket
import SocketServer
import time
from marshal import dumps, loads
import time

<<<<<<< HEAD
#Some globals
#@des:   The RemoteSystem class is responsible for making connections between
#        Primary and Secondary system for the exchange of data
#@param: data_type, a string representing the TYPE of data expected
#        appropriate TYPE include: "INIT", "FINAL"
class RemoteSystem(SocketServer.BaseRequestHandler):
   def __init__(self, data_type):
      self.data_type = data_type
      self.port = 9011
      self.data = dumps(dict())
      self.hash_data = dict()

   #@des:   The client is responsible for deserializing an object and 
   #        connecting to the specified ip to receive some data from
   #        the server. If there is no server listening on the ip specified
   #        the client waits for some period of time then attempts to reconnect
   #@param: ip, ip of the listening server
   def client(self, ip):
      #Create a TCP socket
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      retry = True
      count = 0
      #Initiate connection
      while(retry == True):
         try:
            retry = False
            sock.connect((ip,self.port))
         except socket.error:
            if(count < 5 ):
               retry = True
               count += 1
               logger.subsection("listening server not ready. retrying in 2 mins...")
               time.sleep(120)
         except socket.timeout:
            exit.open("could not connect to remote server")
         except:
            exit.open("a major connection error has occured. check your address and retry installation.")
      #Receive data from server
      self.data = sock.recv(self.port)
      sock.close
      #Convert serialized object to dictionary
      self.hash_data = loads(self.data)
      try:
         if(hash_data['TYPE'] != self.data_type):
            exit.open("primary and secondary server out of sync, restart installation")
      except:
         exit.open("failed to read remote data configuration restart installation")
      return self.hash_data
=======
# Serialized object representation of dictionary
DICT = dumps(dict())

# Python's TCP Handler class
class MyTCPHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    # Log client IP address
    # logger.subsection("client connected from address %s") % self.client_address[0]
    # Send serialized dictionary object to client
    self.request.send(DICT)
>>>>>>> himanshu-database/master

class RemoteServices:
  def __init__(self, host="localhost", port=9999):
    self.HOST = host
    self.PORT = port
    self.RESULT = {}

<<<<<<< HEAD
   #@des:   The server is responsible for listening for connections from a 
   #        client and sending data. In the event of 
   #        an error, it resends then quits
   #@param: hash_data, data packet to be sent

   def server(self, hash_data):
      hash_data['TYPE'] = self.data_type #Control flag
      #We serialize the data to be sent
      self.data = dumps(hash_data)
      #Create server and bind to ourselves
      server = SocketServer.TCPServer(("localhost", self.port), RemoteSystem)
      server.handle_request()
      logger.subsection("closing open port: "+self.port)

   def handle(self):
      self.request.send(self.data)
=======
  # Accepts a dictionary to be sent
  def server(self, get_dict):
    global DICT
    DICT = dumps(get_dict)
    # Create the server, binding to given host and port
    server = SocketServer.TCPServer((self.HOST, self.PORT), MyTCPHandler)
    # Activate the server and handle a single request from the client
    server.handle_request()
>>>>>>> himanshu-database/master

  # Returns dictionary received from Server
  def client(self):
    '''
    reconnect_attempts = 5 
    while (reconnect_attempts > 0):
      try:
        # Attempt connection
        sock.connect((self.HOST, self.PORT))
      except socket.error:
        reconnect_attempts -= 1
        #logger.subsection("listening server not ready. retrying in 2 mins...")
        time.sleep(120)
      except socket.timeout:
        exit.open("Could not connect to remote server")
      except:
        exit.open("A major connection error has occured. check your address and retry installation.")
    '''
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Attempt connection
    sock.connect((self.HOST, self.PORT))
    # Receive serialized dictionary object from the server
    serial_dict = sock.recv(self.PORT)
    # Close socket
    sock.close()
    # Convert serialized object to dictionary
    self.RESULT= loads(serial_dict)
    return self.RESULT
