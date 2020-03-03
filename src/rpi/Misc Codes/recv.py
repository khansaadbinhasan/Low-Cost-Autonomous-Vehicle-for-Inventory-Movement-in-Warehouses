'''
This program is used to establish connection with the host using TCP
	--> Assigns port number and buffer size to be used
	--> Establishes connection and keeps listeninng for data
	--> Used to receive command from workstation.
'''

import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 5005 # Port number on which to send data
BUFFER_SIZE = 20 # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)
while 1:
    data = conn.recv(BUFFER_SIZE).decode("UTF-8")
    
    if not data: 
        break

    print ("received data:", str(data))
    conn.send(data)  # echo
conn.close()
