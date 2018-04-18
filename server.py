import socket
import struct
HOST = '127.0.0.1'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print('Server runs at '+HOST+' '+str(PORT))
print('Wait for Connection...')
 
conn, addr = s.accept()
print('Connected by '+addr[0])
with open('A.mp3','rb') as f:
    while True:
        data=f.read(1460)
        data_len=len(data)
        data_head=struct.pack('i',data_len)
        conn.send(data_head+data)
        if(len(data)<1460) :
            data_head=struct.pack('i',0)
            conn.send(data_head)
            break

# conn.close()