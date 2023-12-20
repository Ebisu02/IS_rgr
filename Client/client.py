import random
import socket as _socket

from utils import *

random.seed(1)

class Client:
    def __init__(self, name: str):
        self.name = name
        self._bufferSize = 1024

    def register(self, host: str='localhost', port: int=3000):
        print(f"[CLIENT_LOG] User \"{self.name}\" trying connect to server for sign up...")
        socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        socket.connect((host, port))
        print(f"[CLIENT_LOG] User \"{self.name}\" successufully connected to server")
        n = int(socket.recv(self._bufferSize).decode(encoding="utf8"))
        print(f"[CLIENT_LOG] Variable 'n' successfully recieved from server")
        socket.send(bytes("{register}", encoding="utf8"))
        socket.send(bytes(self.name, encoding="utf8"))
        self.s = gen_mprime(n)
        v = ext_gcd(self.s, 2, n)
        socket.send(bytes(str(v), encoding="utf-8"))
        status = socket.recv(self._bufferSize).decode("utf8")
        if status == "Success":
            print(f"[CLIENT-LOG] User successfully signed up")
        elif status == "Fail":
            print(f"[CLIENT-LOG] User registration failed, nickname - {self.name}")
        print(f"[CLIENT-LOG] Connection closed\n")
        socket.close()

    def authenticate(self, host: str="localhost", port: int=3000):
        print(f"[CLIENT_LOG] User \"{self.name}\" trying connect to server for sign up...")
        socket = _socket.socket()
        socket.connect((host, port))
        print(f"[CLIENT_LOG] Get connect with server")
        socket.send(bytes("{auth}", encoding="utf8"))
        n = int(socket.recv(self._bufferSize).decode("utf8"))
        print(f"[CLIENT_LOG] Variable 'n' successfully recieved from server")
        socket.send(bytes(self.name, encoding="utf8"))

        while True:
            r = random.randrange(1, n - 1)
            x = ext_gcd(r, 2, n)
            socket.send(bytes(str(x), encoding="utf8"))
            e = int(socket.recv(self._bufferSize).decode("utf8"))
            y = r * self.s ** e % n
            socket.send(bytes(str(y), encoding="utf8"))
            status = socket.recv(self._bufferSize).decode("utf8")
            if status == "Success":
                print("[CLIENT_LOG] Authenticated")
                break
            elif status == "Fail":
                print("[CLIENT_LOG] Authentication denied")
                break
            else:
                pass
                break

        print(f"[CLIENT_LOG] Connection closed\n")
        socket.close()


def simulation_test():
    a = Client('Alice')
    a.register()
    a.authenticate()

    print("\n**** Trying to connect as ALICE by fake user ****\n")

    # Fake user
    mf = Client('Alice')
    mf.s = 12345
    mf.authenticate()


if __name__ == '__main__':
    simulation_test()
