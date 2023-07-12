import socket, threading, pickle, time, pygame, gc
from threading import Thread
from settings import *
from utilities import *

class Client:
    def __init__(self, multiplayer):

        self.multiplayer = multiplayer

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = 'localhost'
        self.port = 5999
        self.addr = (self.ip, self.port)

        self.state = None

        self.response = {'0': None, '1': None, '2': None, '3': None}

        self.mainThread = Thread(target=self.receive)

    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f'[CLIENT] Client is connected to: {self.ip}:{self.port}')

            return True
        except:
            print('[CLIENT] Server doesnt exist.')
            pygame.event.post(pygame.event.Event(backToMenu))
            pygame.event.post(pygame.event.Event(clientDisconnect))

            return False



    def receive(self):
        print('[CLIENT] Listening...')
        while True:
            try:
                serverReceive = self.client.recv(1024)
                try:
                    data_package = pickle.loads(serverReceive)
                    #print(f'[CLIENT] Data received: {data_package}')

                    if data_package[0] == '[GAME DATA]':
                        # TODO get information about collisions and box destroyed

                        try:
                            self.response[str(data_package[1]['index'])] = data_package[1]
                        except:
                            print('[CLIENT] Parse error')

                    if data_package[0] == '[LOBBY DATA INITIAL]':
                        if self.state == None:
                            self.state = data_package
                        else:
                            self.state[2] = data_package[2]
                            self.state[3] = data_package[3]

                        self.multiplayer.updateState()

                    if data_package[0] == '[LOBBY DATA]':

                        self.state[2] = data_package[1]
                        self.state[3] = data_package[2]

                        self.multiplayer.updateState()


                    if data_package == '[LOBBY END]':
                        self.multiplayer.gameInit()

                    if data_package == '[PLAYER LIMIT]':
                        print('[CLIENT] Connection refused. (Server is at max players)')
                        pygame.event.post(pygame.event.Event(backToMenu))
                        pygame.event.post(pygame.event.Event(clientDisconnect))

                    if data_package == '[ALREADY IN GAME]':
                        print('[CLIENT] Connection refused. (Game has already started)')
                        pygame.event.post(pygame.event.Event(backToMenu))
                        pygame.event.post(pygame.event.Event(clientDisconnect))


                except socket.error as ex:
                    print(f'[CLIENT ERROR] Packet lost... ({ex})')

            except socket.error as ex:
                print(f'Lost connection to the server! ({ex})')
                break

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
                gc.collect()

            pygame.event.post(pygame.event.Event(backToMenu))
            pygame.event.post(pygame.event.Event(clientDisconnect))


        except socket.error as ex:
            print(ex)


    def run(self):
        self.mainThread.start()

