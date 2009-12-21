import SocketServer
from marshal import dumps

# Serialized object representation of dictionary
DICT = dumps(dict())

class MyTCPHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    # Send serialized dictionary object to client
    self.request.send(DICT)

def intialize(get_dict):
  global DICT
  DICT = dumps(get_dict)
  HOST, PORT = "localhost", 9999
   
  # Create the server, binding to localhost on port 9999
  server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
  
  # Activate the server, handle a single request from the client and then stop
  server.handle_request()
