import sys
import socket
HOST = '172.18.33.5'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    msg_send=input("Input msg to send")
    s.send(bytes(msg_send,'utf8'))
    print("Waiting to msg")
    data = s.recv(1024)
    print ("Msg received")
    print(str(data,'utf8'))
    

    #s.close()