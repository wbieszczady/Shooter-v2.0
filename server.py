import socket, pickle, time, threading
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

        self.bind()

    def bind(self):
        try:
            self.server.bind(self.addr)

            self.startThread = Thread(target=self.run)
            self.startThread.start()

        except socket.error as ex:
            print(f'[BIND] {ex}')

    def handle_client(self, client, player_index):

        print(f'[SERVER INFO] New connection! (Player index: {player_index})')

        msg = pickle.dumps([player_index, self.count])
        client.send(msg)

        connected = True
        while connected:
            try:
                serverReceived = client.recv(1024)
                try:
                    data_package = pickle.loads(serverReceived)
                except:
                    print('[SERVER INFO] Packet Lost...')

                print(f'[SERVER INFO] Data received: {data_package}')

                dataToSend = [player_index, data_package]
                self.broadcast(dataToSend, client)

            except Exception as ex:
                break


        print(f'[SERVER INFO] Lost connection to: {player_index}')
        self.count -= 1
        client.close()

        for key in self.clients.keys():
            if key == str(player_index):
                self.clients[key] = None



    def broadcast(self, data, thisClient):
        data_package = pickle.dumps(data)

        for k, v in self.clients.items():
            if v != thisClient and v != None:
                try:
                    self.clients[k].sendall(data_package)
                except socket.error as ex:
                    print(f'[BROADCAST] {ex}')

    def run(self):
        print(f'[SERVER INFO] Server is listening... [{self.ip}]')
        self.server.listen(1)
        while True:
            try:
                client, addr = self.server.accept()
                self.count += 1

                for k, v in self.clients.items():
                    if v == None:
                        player_index = k
                        self.clients[k] = client
                        break

                thread = Thread(target = self.handle_client, args = (client, int(player_index)))
                print(f'[SERVER INFO] Clients connected: {self.count}')
                thread.start()
            except socket.error as ex:
                print(f'\n[CLIENT] {ex}')
                break

    def shutServer(self):
        try:
            print('\n[SERVER INFO] Server is shutting down...')

            self.server.close()

            for k, v in self.clients.items():
                if v != None:
                    self.clients[k].close()

            self.startThread.join()

            print('[SERVER INFO] Server has shut down.')

        except Exception as ex:
            print(f'[SHUTTING DOWN] {ex}')