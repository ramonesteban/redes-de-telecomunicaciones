import socket

s = socket.socket()
s.bind(('localhost', 9999))
s.listen(1)

print 'Waiting client'
sc, addr = s.accept()

while True:
  received = sc.recv(1024)
  print 'Received:', received
  if received == 'quit':
    break
  sc.send('ACK')

print 'Sesion expired'
sc.close()
s.close()
