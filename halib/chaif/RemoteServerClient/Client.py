#! /usr/bin/env python
#
# Copyright (c) 2009 Himanshu CHhetri <himanshuchhetri@gmail.com> 
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
import sys
from marshal import loads

def intialize(server="localhost", port=9999):
  HOST, PORT = server, port

  # Create a TCP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  sock.connect((HOST, PORT))

  # Receive serialized dictionary object from the server and shut down
  DICT = sock.recv(PORT)
  sock.close()

  # Get dictionary from serialized object
  get_dict = loads(DICT)

  return get_dict
