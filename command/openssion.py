# encoding: utf-8
from ctypes import *
import struct
from others import *

class Openssion_Req():
    def __init__(self):
        self.step=1
        self.cipherid=17
        self.remoteConsoleSessionID=192
        self.managedSystemSessionID=168
        self.typeStr='=BBII'

class Openssion_Res:
    def __init__(self,stepResponse,ccode,rand_console,rand_bmc,len_cert,cert):
        self.stepResponse=stepResponse
        self.ccode=ccode
        self.rand_console=rand_console
        self.rand_bmc=rand_bmc
        self.len_cert=len_cert
        self.cert=cert
        self.typeStr='=BBIIBp'

def openssion(udp_socket):
    try:
        recv_data,addr = udp_socket.recvfrom(1024)  # 1024表示本次接收的最大字节数
        print("from:",addr)
        ss = Openssion_Req()
        recdata = struct.unpack(ss.typeStr,recv_data)#接受bmc请求
        print(recdata)
        if recdata[0]!=1:                             #查看是否为opensession请求
            raise ConnectError("openssion error:wrong steps")
        session.conselonid=recdata[2]
        session.bmcid=recdata[3]
        session.cipherid=recdata[1]

        send_data="dsfsdtr"                           #返回给bmc信息，0代表成功
        send_struct = Openssion_Res(1,0,234,456,len(send_data),send_data)
        
    except ConnectError,e:
        print(e.error)
        send_struct = Openssion_Res(1,1,234,456,len(e.error),e.error)

    finally:
        send_data=struct.pack(
            send_struct.typeStr,
            send_struct.stepResponse,
            send_struct.ccode,
            send_struct.rand_console,
            send_struct.rand_bmc,
            send_struct.len_cert,
            send_struct.cert)
        udp_socket.sendto(send_data,addr)
        #udp_socket.close()
        if send_struct.ccode==0:
            print("openssion done\n")
            return recdata[2],recdata[3]
        else:
            print("openssion error\n")