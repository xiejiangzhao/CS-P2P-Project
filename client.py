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
def Build_Head(service_Type,service_Num,Version,data_len):
    return struct.pack('hhhh',service_Type,service_Num,Version,data_len)
def Connect():
    try:
        session.connect((HOST, PORT))
    except:
        print("Connect Failed")
    return

def List_Dict():
    data_head=Build_Head(0,0,1,0)
    session.send(data_head)
    response_head=recv(session,8)
    length=struct.unpack('hhhh',response_head)[3]
    response=recv(session,length)
    data=pickle.loads(response)
    print("当前目录有以下文件:")
    for file_name in data:
        print(file_name)
    return

def Down_File(filename):
    with open("filename",'rb') as f:
        file_data=f.read(1460)
        while len(file_data)>0:
            data_head=Build_Head(1,0,1,len(file_data))
            session.send(data_head+file_data)
        f.close()

def Terminal():
    command=input(">>>")
    while command!='exit':
        if command=='ls':
            List_Dict()
        elif command=='download':
            filename=input("输入文件名:"):
            Down_File(filename)
        else:
            print("命令未找到")
        command=input(">>>")

def recv(obj,length):
    data=b''
    while len(data)<length:
        data+=obj.recv(length-len(data))
    return data

Connect()
Terminal()
session.close()

