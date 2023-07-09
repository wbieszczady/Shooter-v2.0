import socket, threading, pickle, time, pygame
from threading import Thread
from settings import *

class Client:
    def __init__(self, multiplayer):

        self.multiplayer = multiplayer

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = 'localhost'
        self.port = 5999
        self.addr = (self.ip, self.port)

        self.packet_test = {'message': 'huj',
                            'test': 4
                            }

        self.state = None
        self.response = None

        self.mainThread = Thread(target=self.receive)

        self.connect()

    def connect(self):
        self.client.connect(self.addr)
        print(f'[CLIENT] Client is connected to: {self.ip}:{self.port}')


    def receive(self):
        print('[CLIENT] Listening...')
        while True:
            try:
                serverReceive = self.client.recv(1024)
                try:
                    data_package = pickle.loads(serverReceive)
                    print(f'[CLIENT] Data received: {data_package}')

                    if data_package[0] == '[GAME DATA]':
                        self.response = data_package

                    if data_package[0] == '[LOBBY DATA]':
                        if self.state == None:
                            self.state = data_package
                        else:
                            self.state[2] = data_package[2]
                            self.state[3] = data_package[3]

                    if data_package == '[LOBBY END]':
                        self.multiplayer.gameInit()

                except socket.error as ex:
                    print(f'[CLIENT ERROR] Packet lost... ({ex})')

            except socket.error as ex:
                print(f'Lost connection to the server! ({ex})')
                break
                self.disconnect()

    def sendNickname(self):
        data_package = ['[NICKNAME]', GAME_NICKNAME]
        self.send(data_package)

    def send(self, msg):
        data_package = pickle.dumps(msg)
        try:
            self.client.sendall(data_package)
        except socket.error as ex:
            print('[CLIENT ERROR] Lost connection to the server!')
            self.disconnect()

    def disconnect(self):

        print('[CLIENT] Connection breaks...')

        try:

            self.client.close()

            if self.mainThread.is_alive():
                self.mainThread.join()


        except socket.error as ex:
            print(ex)


    def run(self):
        self.mainThread.start()

