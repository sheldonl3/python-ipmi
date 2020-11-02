# encoding: utf-8
from socket import *
import openssion

class TTP():
    def __init__(self,bmc_ip):
        self.bmc_ip=bmc_ip
        self.port=12346

    def set_socket(self):
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        dest_addr = (self.bmc_ip, self.port)
        #udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        udp_socket.bind(dest_addr)
        self.socket=udp_socket


if __name__=="__main__":
    ttp=TTP('127.0.0.1')
    ttp.set_socket()
    while True:
        openssion.openssion(ttp.socket)