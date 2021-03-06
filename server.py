import socket
import struct
import os
import pickle
import ssl
import threading
HOST = input("Input HOST:")
PORT = int(input("Input PORT:"))
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain(certfile="mycertfile.pem", keyfile="mykeyfile.pem")
session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
session.bind((HOST, PORT))
session.listen(3)
service_Type=None
service_Num=None
Version=None
data_len=None


def Build_Head(service_Type,service_Num,Version,data_len):
    return struct.pack('hhhh',service_Type,service_Num,Version,data_len)

def Creat_Connect():
    print("Waiting for connection")
    connect,addr=session.accept()
    ssl_conn = context.wrap_socket(connect, server_side=True)
    print("Connect to "+str(addr))
    return ssl_conn,addr

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

def Send_Dict(connect):
    files_data=pickle.dumps(os.listdir("./"))
    service_Type=0
    service_Num=0
    Version=1
    data_len=len(files_data)
    data_head=struct.pack('hhhh',service_Type,service_Num,Version,data_len)
    connect.send(data_head+files_data)

def Send_File(connect,filename_len):
    filename_byte=recv(connect,filename_len)
    filename=pickle.loads(filename_byte)
    file_len_sum=0
    if not os.path.exists(filename):
        data_head=Build_Head(1,1,1,-1)
        connect.send(data_head)
        return
    with open(filename,'rb') as f:
        file_data=b'0'
        while len(file_data)!=0:
            file_data=f.read(1460)
            data_head=Build_Head(1,1,1,len(file_data))
            file_len_sum+=len(file_data)
            connect.send(data_head+file_data)
        print("传输结束,共"+str(file_len_sum)+"个字节")
        f.close()

def Save_File(connect,filename_len):
    filename_byte=recv(connect,filename_len)
    filename=pickle.loads(filename_byte)
    file_len_sum=0
    with open(filename,'wb+') as f:
        file_data=b''
        file_len=struct.unpack('hhhh',recv(connect,8))[3]
        while file_len>0:
            file_len_sum+=file_len
            file_data=recv(connect,file_len)
            f.write(file_data)
            file_len=struct.unpack('hhhh',recv(connect,8))[3]
        print("传输结束,共"+str(file_len_sum)+"个字节")
    f.close()
    pass
def Del_File(connect,filename_len):
    filename_byte=recv(connect,filename_len)
    filename=pickle.loads(filename_byte)
    info="成功删除"
    try:
        os.remove(filename)
    except:
        info="删除失败"
    info_byte=pickle.dumps(info)
    data_head=Build_Head(0,1,1,len(info_byte))
    connect.send(data_head+info_byte)
def Task(connect,addr):
    while True:
        request_head=recv(connect,8)
        head_data=struct.unpack('hhhh',request_head)
        if comp(head_data,(0,0,1)):
            print("Send file list to "+addr[0]+":"+str(addr[1]))
            Send_Dict(connect)
        elif comp(head_data,(1,0,1)):
            print("Send file to "+addr[0]+":"+str(addr[1]))
            Send_File(connect,head_data[3])
        elif comp(head_data,(0,1,1)):
            print("Del file order by "+addr[0]+":"+str(addr[1]))
            Del_File(connect,head_data[3])
        elif comp(head_data,(1,2,1)):
            print("Save file from "+addr[0]+":"+str(addr[1]))
            Save_File(connect,head_data[3])
        elif comp(head_data,(2,3,3)):
            print("Close connection by "+addr[0]+":"+str(addr[1]))
            break
        else:
            print("Unknown")

while True:
    conn_thread,addr=Creat_Connect()
    new_thread=threading.Thread(target=Task,args=(conn_thread,addr))
    new_thread.start()

