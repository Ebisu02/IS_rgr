import json
import signal
import socket as _socket
import signal as _signal

from utils import *

class Server:
    def __init__(self, host: str="localhost", port: int=3000):
        self._host = host
        self._port = port
        self._bufferSize = 1024

        p = q = get_prime(1 << 1023, (1 << 1024) - 1)
        while p == q:
            q = get_prime(1 << 1023, (1 << 1024) - 1)
        self.n = p * q
        print(f"[SERVER_LOG] {p = }, {q = }, {self.n = }")

        try:
            with open("users.json", "r") as f:
                self._users = json.load(f)
            print("[SERVER_LOG] Users database successfully downloaded")
        except FileNotFoundError:
            with open("users.json", "w") as f:
                self._users = dict()
                json.dump(self._users, f)
            print("[SERVER_LOG] Warning: cant download users database. Created new")

    def run(self):
        socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        socket.bind((self._host, self._port))
        socket.listen()
        print("[SERVER_LOG] Server started")

        while True:
            connection, address = socket.accept()
            print(f"\n[SERVER_LOG] New connection: {address}")
            connection.send((bytes(str(self.n), encoding="utf8")))
            print(f"[SERVER_LOG] Sended variable \"n\" to user {address}")
            data = connection.recv(self._bufferSize).decode("utf8")

            if data == "{register}":
                name = connection.recv(self._bufferSize).decode("utf8")
                v = int(connection.recv(self._bufferSize).decode("utf8"))

                if name not in self._users.keys():
                    print(f"[SERVER_LOG] User {address} successfully signed up with login \"{name}\" and with key: {v = }")
                    self._users[name] = v
                    with open("users.json", "w") as f:
                        json.dump(self._users, f)
                    connection.send((bytes("Success", encoding="utf8")))
                else:
                    print(f"[SERVER_LOG] User with {name = } already signed up")
                    connection.send((bytes("Fail", encoding="utf8")))

            if data == "{auth}":
                name = connection.recv(self._bufferSize).decode("utf8")
                v = self._users[name]
                print(f"[SERVER_LOG] User {address} trying to connect with {name = }")
                print(f"[SERVER_LOG] Authentication process:")
                t = 20
                #print("[]ABC")
                for i, _ in enumerate(range(t), 1):
                    x = int(connection.recv(self._bufferSize).decode("utf8"))
                    # print(f"[]e = ")
                    e = random.randint(0, 1)
                    #e = 3
                    connection.send((bytes(str(e), encoding="utf8")))
                    y = int(connection.recv(self._bufferSize).decode("utf8"))
                    y2 = ext_gcd(y, 2, self.n)
                    xv = x * ext_gcd(v, e, self.n) % self.n
                    print(f"[SERVER_LOG] {i}. {x = }; {e = }; {y = }; t(y^2)%n = {y2}; (tx*v^e)%n = {xv}")

                    if y2 == xv:
                        print(f"[SERVER_LOG] Success! y^2 == x * v^e % n")
                        print(f"[SERVER_LOG] Authenticated = \"{name}\"")
                        connection.send(bytes("Success", encoding="utf8"))
                        break
                    else:
                        print(f"[SERVER_LOG] Fail! y^2 != x * v^e % n")
                        connection.send((bytes("Fail", encoding="utf8")))
                        print(f"[SERVER_LOG] Fake user - {address} didnt authenticated")
                        break
            connection.close()
            print(f"[SERVER_LOG] Connection closed")


def simulate():
    _signal.signal(signal.SIGINT, signal.SIG_DFL)
    server = Server()
    server.run()


if __name__ == "__main__":
    simulate()

