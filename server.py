import socket
import struct
import os
import pickle
HOST = '127.0.0.1'
PORT = 8002
session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
service_Type=None
service_Num=None
Version=None
data_len=None
def Creat_Connect():
    session.bind((HOST, PORT))
    session.listen(1)
    print("Waiting for connection")
    connect,addr=session.accept()
    print("Connect to "+str(addr))
    return connect

connect=Creat_Connect()
def recv(obj,length):
    data=b''
    while len(data)<length:
        data+=obj.recv(length-len(data))
    return data

def comp(tuple1,tuple2):
    for i in range(3):
        if tuple1[i]!=tuple2[i]:
            return False
    return True

def Send_Dict():
    files_data=pickle.dumps(os.listdir("./"))
    service_Type=0
    service_Num=0
    Version=1
    data_len=len(files_data)
    data_head=struct.pack('hhhh',service_Type,service_Num,Version,data_len)
    connect.send(data_head+files_data)

def Send_File():
    pass
while True:
    request_head=recv(connect,8)
    head_data=struct.unpack('hhhh',request_head)
    if comp(head_data,(0,0,1)):
        Send_Dict()
    elif comp(head_data,(1,0,1)):
        Send_File()
    else:
        a=input()

