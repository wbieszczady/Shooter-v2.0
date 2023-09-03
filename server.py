import socket, pickle, time, threading, gc
import sys
from threading import Thread


class Server:
    def __init__(self):
        self.ip = 'localhost'
        self.port = 5999

        self.addr = (self.ip, self.port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.count = 0

        self.clients = {
            '0': None,
            '1': None,
            '2': None,
            '3': None
        }

        self.clientsNicknames = {
            '0': None,
            '1': None,
            '2': None,
            '3': None
        }

        self.inGame = False


    def bind(self):
        try:
            self.server.bind(self.addr)

            self.startThread = Thread(target=self.run)
            self.startThread.start()

            return True

        except socket.error as ex:

            print(f'[SERVER ERROR] {ex}')
            return False

    def handle_client(self, client, player_index):

        print(f'[SERVER] New connection! (Player index: {player_index})')

        connected = True
        while connected:
            try:
                serverReceived = client.recv(1024)
                try:
                    data_package = pickle.loads(serverReceived)
                    #print(f'\r[SERVER] Data received: {data_package}')

                    self.packageParser(client, player_index, data_package)


                except socket.error as ex:
                    print(f'[SERVER ERROR] Packet Lost... ({ex})')

            except socket.error as ex:
                print('[SERVER ERROR] Something went wrong with a client parser.')
                print(f'[SERVER ERROR] {ex}')
                break

        self.clientDisconnect(client, player_index)
    def packageParser(self, client, player_index, data_package):

        if data_package[0] == '[GAMEDATA-1]':
            self.broadcast(data_package, client, player_index)

        if data_package == '[GAMEDATA-2]':
            self.broadcastAll(data_package, player_index)

        if data_package[0] == '[NICKNAME]':
            self.acceptNickname(data_package, player_index)

        if data_package == '[LOBBY END]':
            self.lobbyEnd(data_package)
            self.inGame = True

    def broadcastAll(self, data, player_index):

        data_package = pickle.dumps([data, player_index])

        for k, v in self.clients.items():
            if v != None:
                self.clients[k].sendall(data_package)



    def broadcast(self, data, thisClient, player_index):

        data_package = pickle.dumps(data)

        for k, v in self.clients.items():
            if v != thisClient and v != None:
                try:
                    self.clients[k].sendall(data_package)
                except:
                    print(f'[SERVER ERROR] Broadcast problem...')


    def acceptNickname(self, data_package, player_index):

        #changing nickname list
        for key in self.clientsNicknames.keys():
            if key == str(player_index):
                self.clientsNicknames[key] = data_package[1]

        #sending changes to other clients
        self.sendLobbyData(player_index)

    def sendLobbyData(self, player_index):

        msg = ['[LOBBY DATA INITIAL]', player_index, self.count, self.clientsNicknames]
        data_package = pickle.dumps(msg)

        for k, v in self.clients.items():
            if v != None:
                self.clients[k].sendall(data_package)

    def updateLobbyData(self):
        msg = ['[LOBBY DATA]', self.count, self.clientsNicknames]
        data_package = pickle.dumps(msg)

        for k, v in self.clients.items():
            if v != None:
                self.clients[k].sendall(data_package)

    def lobbyEnd(self, msg):

        data_package = pickle.dumps(msg)
        for k, v in self.clients.items():
            if v != None:
                self.clients[k].sendall(data_package)



    def clientDisconnect(self, client, player_index):

        print(f'[SERVER] Lost connection to: {player_index}')
        self.count -= 1

        client.close()

        for key in self.clients.keys():
            if key == str(player_index):
                self.clients[key] = None

        for key in self.clientsNicknames.keys():
            if key == str(player_index):
                self.clientsNicknames[key] = None

        self.updateLobbyData()


    def run(self):
        print(f'[SERVER] Server is listening... [{self.ip}]')
        while True:
            try:

                self.server.listen(3)

                client, addr = self.server.accept()

                if self.count < 4 and not self.inGame:

                    self.count += 1

                    for k, v in self.clients.items():
                        if v == None:
                            player_index = k
                            self.clients[k] = client
                            break

                    print(f'[SERVER] Clients connected: {self.count}')

                    thread = Thread(target = self.handle_client, args = (client, int(player_index)))
                    thread.start()

                elif self.count == 4:
                    msg = '[PLAYER LIMIT]'
                    data_package = pickle.dumps(msg)
                    client.send(data_package)
                elif self.inGame:
                    msg = '[ALREADY IN GAME]'
                    data_package = pickle.dumps(msg)
                    client.send(data_package)



            except socket.error as ex:
                print(f'\n[SERVER ERROR] Client connection problem...')
                break

    def shutServer(self):
        try:
            print('\n[SERVER] Server is shutting down.')

            self.server.close()

            for k, v in self.clients.items():
                if v != None:
                    self.clients[k].close()

            self.startThread.join()
            gc.collect()


            print('[SERVER] Server has shut down.')

        except Exception as ex:
            print(f'[SERVER] Disconnect problem...')