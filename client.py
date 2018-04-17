import sys
import socket
HOST = '127.0.0.1'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

with open('a.md','wb+') as target:
    target.write(s.recv(1024))
    

    #s.close()