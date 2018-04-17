import sys
import socket
HOST = '127.0.0.1'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data_allrecv=b''
recv_file=open('B.mp3','ab+')
while True:
    data_recv=s.recv(1460)
    recv_file.write(data_recv)
    print("get")
    if(len(data_recv)<1460):
        break
    
recv_file.close()
    #s.close()