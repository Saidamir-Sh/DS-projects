import random
import socket

# create a socket and bind it to a specific address and port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 12345))

# listen for incoming connections
s.listen()
conn, addr = s.accept()

# generate random numbers and send them to the consumer via the socket
while True:
    number = random.randint(1, 100)
    conn.sendall(str(number).encode())
    if number == 0:
        break

# send the 'FINISH' signal to signal the end of the sequence
conn.sendall(b'FINISH')

# close the connection
conn.close()
