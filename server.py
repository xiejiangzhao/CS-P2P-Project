import socket

HOST = '192.168.199.198'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print('Server runs at '+HOST+' '+str(PORT))
print('Wait for Connection...')
 
while True:
    conn, addr = s.accept()
    print('Connected by '+addr[0])

    while True:
        msg_send=input("Input msg to send")
        conn.send(bytes(msg_send,'utf8'))
        print("Waiting to msg")
        data = conn.recv(1024)
        print ("Msg received")
        print(str(data,'utf8'))
        
        

# conn.close()