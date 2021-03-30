import socket

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)

print(hostname)
print(ip_addr)