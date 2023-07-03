import socket, pickle, time, threading
from threading import Thread


class Server:
    def __init__(self):
        self.ip = 'localhost'
        self.port = 5999

        self.addr = (self.ip, self.port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = {
            '0': None,
            '1': None,
            '2': None,
            '3': None
        }

        self.bind()

    def bind(self):
        try:
            self.server.bind(self.addr)

            self.startThread = Thread(target=self.run)
            self.startThread.start()

        except socket.error as ex:
            print(f'[BIND] {ex}')

    def handle_client(self, client, player_index):

        print(f'New connection! (Player index: {player_index})')

        msg = pickle.dumps(player_index)
        client.send(msg)

        connected = True
        while connected:
            try:
                serverReceived = client.recv(1024)
                data_package = pickle.loads(serverReceived)

                print(f'Data received: {data_package}')

                dataToSend = [player_index, data_package]
                self.broadcast(dataToSend, client)

            except:
                break
        print(f'Lost connection to: {player_index}')

        for key in self.clients.keys():
            if key == str(player_index):
                self.clients[key] = None

        connected = False
        client.close()



    def broadcast(self, data, thisClient):
        data_package = pickle.dumps(data)

        for k, v in self.clients.items():
            if v != thisClient and v != None:
                try:
                    self.clients[k].sendall(data_package)
                except socket.error as ex:
                    print(f'[BROADCAST] {ex}')

    def run(self):
        print(f'Server is starting... [{self.ip}]')
        self.server.listen(4)
        while True:
            try:
                client, addr = self.server.accept()

                for k, v in self.clients.items():
                    if v == None:
                        player_index = k
                        self.clients[k] = client
                        break

                thread = Thread(target = self.handle_client, args = (client, player_index))
                print(f'Clients connected: {threading.active_count()}')
                thread.start()
            except socket.error as ex:
                print(f'[CLIENT] {ex}')
                break

    def shutServer(self):
        try:
            print('\nServer is shutting down...')

            # self.server.shutdown(socket.SHUT_RDWR)
            self.server.close()

        except Exception as ex:
            print(f'[SHUTTING DOWN] {ex}')