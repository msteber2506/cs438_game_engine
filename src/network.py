
import socket
import sys

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


class Client:
    def __init__(self):
        pass

    def start_client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        message = "hello"
        s.sendall(message.encode())
        response = s.recv(1024)
        print("Received:", repr(response.decode()))


if __name__ == "__main__":
    argv = sys.argv[1:]

    if argv[0] == "c":
        client = Client()
        client.start_client()
    else:
        server = Server(HOST, PORT)
        server.start_server()
