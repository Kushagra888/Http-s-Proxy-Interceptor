import socket
import threading
import tkinter


class Proxy:
    PacketQueue = []
    PacketQueueLock = threading.Lock()
    RECV_MSG_LEN = 1024

    def __init__(self, port=8080, hostName="127.0.0.1"):
        self.port = port
        self.host = hostName
        try:
            # Create a socket to accept all client connections
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
        except socket.error as e:
            print("Error creating Proxy socket", e)
            exit(1)

    def start(self, gui):

        self.server.listen(5)
        print("[*] Listening on " + str(self.host) + ":" + str(self.port))
        thread = threading.Thread(target=self.acceptConnections, args=(gui,))
        thread.start()
        gui.start()

    def acceptConnections(self, gui):
        try:
            while True:
                client, addr = self.server.accept()
                print("[*] Connection from: " + str(addr))
                client.settimeout(10)
                # Adding into the proxy paket queue
                with Proxy.PacketQueueLock:
                    Proxy.PacketQueue.append(client)

                if not gui.request_text.get(1.0, tkinter.END).strip():
                    gui.loadNewRequest()
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print("[*] Exception: " + str(e))
            exit(1)

    @classmethod
    def getRequest(cls, client_socket):
        request = b""
        while True:
            try:
                data = client_socket.recv(cls.RECV_MSG_LEN)
                request += data
                if not data or len(data) < cls.RECV_MSG_LEN:
                    break
            except socket.timeout:
                break
        return request

    @classmethod
    def terminateConnection(cls, client):
        print("[*] Closed connection to: " + str(client.getpeername()))
        client.shutdown(socket.SHUT_RDWR)
        client.close()

    @classmethod
    def getResponse(cls, request):
        host, port = Proxy.extractHostAndPort(request)

        proxy2RemoteServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(20)
        proxy2RemoteServer.connect((host, port))
        proxy2RemoteServer.send(request.encode("utf8"))

        response = b""

        while True:
            try:
                data = proxy2RemoteServer.recv(cls.RECV_MSG_LEN)
                response = response + data
                if data == b"" or len(data) < cls.RECV_MSG_LEN:
                    break
            except socket.timeout:
                break
        return response

    @classmethod
    def extractHostAndPort(cls, request):
        host = "localhost"
        port = 80
        request = request.split("\n")
        for line in request:
            line = line.strip()
            if "Host:" in line:
                host = line.split(":")[1].strip()
            if "Port:" in line:
                port = int(line.split(":")[1].strip())
        return host, port
