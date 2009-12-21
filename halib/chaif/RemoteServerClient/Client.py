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
