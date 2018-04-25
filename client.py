import sys
import socket
import struct
import pickle
HOST = '127.0.0.1'
PORT = 8002
session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
service_Type=None
service_Num=None
Version=None
data_len=None
def Connect():
    try:
        session.connect((HOST, PORT))
    except:
        print("Connect Failed")
    return

def List_Dict():
    service_Type=0
    service_Num=0
    Version=1
    data_len=0
    data_head=struct.pack('hhhh',service_Type,service_Num,Version,data_len)
    session.send(data_head)
    response_head=recv(session,8)
    length=struct.unpack('hhhh',response_head)[3]
    response=recv(session,length)
    data=pickle.loads(response)
    print("当前目录有以下文件:")
    for file_name in data:
        print(file_name)
    return
def Terminal():
    command=input(">>>")
    while command!='exit':
        if command=='ls':
            List_Dict()
        else:
            print("命令未找到")
        command=input(">>>")

def recv(obj,length):
    data=b''
    while len(data)<length:
        data+=obj.recv(length-len(data))
    return data

Connect()

while True:
    Terminal()

