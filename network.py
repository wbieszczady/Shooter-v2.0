import socket, threading, pickle, time
from threading import Thread


class Client:
    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = 'localhost'
        self.port = 5999
        self.addr = (self.ip, self.port)

        self.packet_test = 'cos tam'

    def connect(self):
        self.client.connect(self.addr)
        print(f'Client is connected to: {self.ip}:{self.port}')
        try:
            serverReceive = self.client.recv(2048)
            data_package = pickle.loads(serverReceive)
            return data_package
        except:
            pass

    def receive(self):
        try:
            serverReceive = self.client.recv(2048)
            data_package = pickle.loads(serverReceive)
            print(f'Data received: {data_package[1]} from {data_package[0]}')
            return data_package
        except:
            pass

    def send(self, msg):
        data_package = pickle.dumps(msg)
        self.client.sendall(data_package)
