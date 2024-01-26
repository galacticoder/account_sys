import socket

hostname = socket.gethostname()
aa = socket.gethostbyname(hostname)
print(aa)