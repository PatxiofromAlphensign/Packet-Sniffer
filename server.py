import socket, fcntl, struct, sys, termios
from itertools import count
# just for demo purposes

def mkiocall(s, msg, i=0):
    nums_that_works = []
    for i in count(1):
        try:
            fcntl.ioctl(s.fileno(),i, b"tet")
            nums_that_works.append(i)
        except:
            if i > 10000:
                break
    i = nums_that_works[0]
    return fcntl.ioctl(s.fileno(),i, b"tet")

with socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) as sock:
    sock.bind((sys.argv[1], 0))
    sb = struct.pack("256s", bytes("enp7s0",encoding="utf8"))
    name = socket.inet_ntoa(fcntl.ioctl(sock.fileno(), 0x8915, sb)[20:24])

def listen(): # TODO do something interesting here
    with socket.socket() as s:
        s.bind((name, 801))
        s.listen()
        print(mkiocall(s, "tucker"))
        while 1:
            conn, addr = s.accept()
            data = conn.recv(12)
            conn.sendall(b"hi bot")
            print("sent data")
        s.close()

listen()

