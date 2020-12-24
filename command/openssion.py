# encoding: utf-8
from ctypes import *
import struct,random
from others import Session

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
        self.typeStr='=BBIII1412s' #s前是大小

def get_rand_num():
    return random.randint(1000,99999)

def openssion(udp_socket):
    session=Session()                           #创建session实例
    recv_data,addr = udp_socket.recvfrom(1024)  #1024表示本次接收的最大字节数
    print("from:",addr)
    ss = Openssion_Req()
    recdata = struct.unpack(ss.typeStr,recv_data)#接受bmc请求
    print(recdata)
    if recdata[0]!=1:                             #查看是否为opensession请求
        print("openssion error:wrong steps")
        return
    session.conselon_id=recdata[2]
    session.bmc_id=recdata[3]
    session.cipher_id=recdata[1]

    cert='''-----BEGIN CERTIFICATE-----
MIIDcDCCAlgCFH8S17vfBLItM6WooqTnv4iULIoAMA0GCSqGSIb3DQEBCwUAMHQx
CzAJBgNVBAYTAkNOMQswCQYDVQQIDAJHRDELMAkGA1UEBwwCU1oxDjAMBgNVBAoM
BXZpaG9vMQwwCgYDVQQLDANkZXYxETAPBgNVBAMMCHZpdm8uY29tMRowGAYJKoZI
hvcNAQkBFgt5eUB2aXZvLmNvbTAeFw0yMDExMTEwMTI4MzFaFw0zMDExMDkwMTI4
MzFaMHUxCzAJBgNVBAYTAkNOMQswCQYDVQQIDAJHRDELMAkGA1UEBwwCU1oxDjAM
BgNVBAoMBXZpaG9vMQwwCgYDVQQLDANkZXYxEjAQBgNVBAMMCWxvY2FsaG9zdDEa
MBgGCSqGSIb3DQEJARYLeXlAdml2by5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDFkVhXMnAZz7zecP6qAr00MoHgGxhDE6SfMi6lBp+d4IslvTTb
T/xgjkYlRMfHIipcYw7hqSKdD8RuW2qfRCrJs363YGMCU5e+hxSY/jMvVLY9OO/9
yZHFb2NIxsoD0wwG55XmS3K2uPjdR3UFPC1Ap1okqu5egAvWYeOG63gJf5me0TgP
CB2pPywygbecOTmRi15qutMN1nFNVKQIrCkz2mqvCVW2A9vtFkDBICatjjxptCSX
V68/Qou3SDt77VBqXJR4LD+uzyR0H0mAypS+EXnFK92fqh9Xhy/e6x19k8+wV8sh
j1ceseRKqBi3TrOz9ee+sD4nsJYaxAm//xOBAgMBAAEwDQYJKoZIhvcNAQELBQAD
ggEBAGTxl3p0EYU06pnV3AKkbMWLX7X2sIdDUHLImPorvkD985KZaykCho6iVDbP
ulRccsk7YrWmmqUKhNJmB9j/Wgs1PQuXdDZqK9WXPmgRu54ve1ogm5hTVhlsGmuO
4tt9E5Y7ZfvZpcnUYEBn79tZEAk/s50thFuAZFHs+FR6kAoV+EbxcspXQiK+ckg1
T9tRaGn8ebuqiXHxi7aCJGlMFiBFS3eVE1ZcRb5dLZMn0p8c4HqN2cW6SjjVP+dO
4XRBLKghByQm3APNgSkg05B9Ukl7Mj0abkA/M7e8zLy8xKnuvkqmARzrExj18UIp
kW0PLLZPEGzMhdxzJnsujdN74g0=
-----END CERTIFICATE-----'''
    session.rand_console=get_rand_num()
    session.rand_bmc=get_rand_num()
    print(session.rand_console,session.rand_bmc)
    send_struct = Openssion_Res(1,0,session.rand_console,session.rand_bmc,len(cert),cert)

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