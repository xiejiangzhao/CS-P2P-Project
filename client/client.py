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
    file_len_sum=0
    with open(filename,'wb+') as f:
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

def Send_File(filename):
    filename_byte=pickle.dumps(filename)
    session.send(Build_Head(1,2,1,len(filename_byte))+filename_byte)
    file_len_sum=0
    with open(filename,'rb') as f:
        file_data=b'0'
        while len(file_data)!=0:
            file_data=f.read(1460)
            data_head=Build_Head(1,3,1,len(file_data))
            file_len_sum+=len(file_data)
            session.send(data_head+file_data)
        print("传输结束,共"+str(file_len_sum)+"个字节")
        f.close()
    f.close()
def Terminal():
    userinput=input(">>>").split()
    command=userinput[0]
    if len(userinput)>1:
        param=userinput[1]
    while command!='exit':
        if command=='ls':
            List_Dict()
        elif command=='download':
            Down_File(param)
        elif command=='del':
            Del_File(param)
        elif command=='upload':
            Send_File(param)
        else:
            print("命令未找到")
        userinput=input(">>>").split()
        command=userinput[0]
        if len(userinput)>1:
            param=userinput[1]

def recv(obj,length):
    data=b''
    while len(data)<length:
        data+=obj.recv(length-len(data))
    return data

Connect()
Terminal()
data_head=Build_Head(2,3,3,0)
session.send(data_head)
session.close()

