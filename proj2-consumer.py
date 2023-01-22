import socket

# create a socket and connect to the address and port of the producer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 12345))

# receive and process the numbers sent by the producer
total = 0
while True:
    data = s.recv(1024).decode()
    if data == 'FINISH':
        break
    total += int(data)

# print the total
print(total)

# close the connection
s.close()

