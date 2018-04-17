import socket

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
        conn.send(data)
        

# conn.close()