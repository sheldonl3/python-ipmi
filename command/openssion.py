# encoding: utf-8
from ctypes import *
from others import *

class Openssion_Req(BigEndianStructure):
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

def openssion(udp_socket):
    try:
        recv_data,addr = udp_socket.recvfrom(1024)  # 1024表示本次接收的最大字节数
        print("from:",addr)
        ss = Openssion_Req()
        ss.decode(recv_data)
        print(ss.step,ss.remoteConsoleSessionID,ss.managedSystemSessionID)
        if ss.step!=1:
            print("openssion error")
            raise ConnectError("openssion error:wrong steps")
 
        send_data = "nihao"
        udp_socket.sendto(send_data.encode(),addr)
        #udp_socket.close()

        print("openssion done\n")
        return ss.remoteConsoleSessionID,ss.managedSystemSessionID
        
    except ConnectError,e:
        print(e.error)
        send_data = "openssion error"
        udp_socket.sendto(send_data.encode(),addr)
        #udp_socket.close()