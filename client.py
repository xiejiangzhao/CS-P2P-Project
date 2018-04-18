import sys
import socket
import struct
HOST = '127.0.0.1'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data_allrecv=b''
recv_file=open('B.mp3','ab+')
while True:
    data_recv=s.recv(4)
    data_len=struct.unpack('i',data_recv[0:15])
    if data_len[0] == 0: break
    while len(data_allrecv)<data_len[0]:
        data_allrecv+=s.recv(data_len[0]-len(data_allrecv))
    recv_file.write(data_allrecv)
    print("get")
    data_allrecv=b''
    
recv_file.close()
    #s.close()