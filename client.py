import socket, threading, pickle, time, pygame
from threading import Thread

class Client:
    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = 'localhost'
        self.port = 5999
        self.addr = (self.ip, self.port)

        self.packet_test = {'message': 'huj',
                            'test': 4
                            }

        self.response = None

    def connect(self):
        self.client.connect(self.addr)
        print(f'Client is connected to: {self.ip}:{self.port}')
        serverReceive = self.client.recv(1024)
        data_package = pickle.loads(serverReceive)
        return data_package


    def receive(self):
        while True:
            try:
                serverReceive = self.client.recv(1024)
                try:
                    data_package = pickle.loads(serverReceive)
                    print(f'Data received: {data_package}')
                except:
                    print(f'[CLIENT] Packet lost...')

                self.response = data_package

            except socket.error as ex:
                print(f'Lost connection to the server! ({ex})')
                break
                self.disconnect()

    def send(self, msg):
        data_package = pickle.dumps(msg)
        try:
            self.client.sendall(data_package)
        except socket.error as ex:
            print('Lost connection to the server!')
            self.disconnect()

    def disconnect(self):

        print('Connection breaks...')

        try:
            self.client.close()
            self.thread.join()

        except socket.error as ex:
            print(ex)

    def run(self):
        self.thread = Thread(target=self.receive)
        self.thread.start()
