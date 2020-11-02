# encoding: utf-8
from ctypes import *
import struct
from others import *

class Openssion_Req():
    def __init__(self):
        self.step=1
        self.remoteConsoleSessionID=192
        self.managedSystemSessionID=168
        self.typeStr='=BII'

class Openssion_Res:
    def __init__(self,stepResponse,rand_console,rand_bmc,len_cert,cert):
        self.stepResponse=stepResponse
        self.rand_console=rand_console
        self.rand_bmc=rand_bmc
        self.len_cert=len_cert
        self.cert=cert
        self.typeStr='=BIIBp'

def openssion(udp_socket):
    try:
        recv_data,addr = udp_socket.recvfrom(1024)  # 1024表示本次接收的最大字节数
        print("from:",addr)
        ss = Openssion_Req()
        recdata = struct.unpack(ss.typeStr,recv_data)

        print(recdata)
        if recdata[0]!=1:
            raise ConnectError("openssion error:wrong steps")

        s="dsfsdtr\n"
        send_struct = Openssion_Res(1,234,456,len(s),s)
        send_data=struct.pack(
            send_struct.typeStr,
            send_struct.stepResponse,
            send_struct.rand_console,
            send_struct.rand_bmc,
            send_struct.len_cert,
            send_struct.cert)
        udp_socket.sendto(send_data,addr)
        #udp_socket.close()

        print("openssion done\n")
        return recdata[1],recdata[2]
        
    except ConnectError,e:
        print(e.error)
        send_data = "openssion error"
        udp_socket.sendto(send_data.encode(),addr)
        #udp_socket.close()