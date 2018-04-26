import sys
import socket
import os
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
    filename_byte=pickle.dumps(filename)
    session.send(Build_Head(1,0,1,len(filename_byte))+filename_byte)
    save_name=input("另存为:")
    file_len_sum=0
    with open(save_name,'wb+') as f:
        file_data=b''
        file_len=struct.unpack('hhhh',recv(session,8))[3]
        while file_len>0:
            file_len_sum+=file_len
            file_data=recv(session,file_len)
            f.write(file_data)
            file_len=struct.unpack('hhhh',recv(session,8))[3]
        print("传输结束,共"+str(file_len_sum)+"个字节")
    f.close()

def Del_File(filename):
    filename_byte=pickle.dumps(filename)
    data_head=Build_Head(0,1,1,len(filename_byte))
    session.send(data_head+filename_byte)
    response_head=recv(session,8)
    length=struct.unpack('hhhh',response_head)[3]
    response=recv(session,length)
    data=pickle.loads(response)
    print(data)
    return

def Terminal():
    command=input(">>>")
    while command!='exit':
        if command=='ls':
            List_Dict()
        elif command=='download':
            filename=input("输入文件名:")
            Down_File(filename)
        elif command=='del':
            filename=input("输入文件名:")
            Del_File(filename)
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

