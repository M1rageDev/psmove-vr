from socket import socket, AF_INET, SOCK_DGRAM
sock = socket(AF_INET, SOCK_DGRAM)
def send(data):
    sock.sendto(data.encode(), ("localhost", 49152))
