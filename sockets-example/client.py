import socket

s = socket.socket()
s.connect(('localhost', 9999))

print 'Write something'
while True:
  message = raw_input('> ')
  if message == 'quit':
    s.send(message)
    break
  s.send(message)
  received = s.recv(1024)
  print 'Response:', received

print 'Sesion expired'
s.close()
