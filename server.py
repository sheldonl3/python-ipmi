# encoding: utf-8
from socket import *
import time
from ctypes import *

class SSHead(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        #(字段名, c类型 )
        ('step', c_uint8),
        ('remoteConsoleSessionID', c_uint32),  #424
        ('managedSystemSessionID', c_uint32),
    ]
    
    def encode(self):
        return string_at(addressof(self), sizeof(self))

    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)


udp_socket = socket(AF_INET, SOCK_DGRAM)

dest_addr = ('127.0.0.1', 12346)
#udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
udp_socket.bind(dest_addr)
while True:
    recv_data,addr = udp_socket.recvfrom(1024)  # 1024表示本次接收的最大字节数
    print("from:",addr)
    #print(recv_data)

    ss = SSHead()
    ss.decode(recv_data)
    print(ss.step,ss.remoteConsoleSessionID,ss.managedSystemSessionID)

    send_data = "nihao"
    udp_socket.sendto(send_data.encode(),addr)

udp_socket.close()
print("quit")