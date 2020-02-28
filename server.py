from socket import *
import sys
import threading
import os

storage = ["NO MSG."]
q = []

def find_open_port(sock):
    s = socket(AF_INET, sock)
    s.bind(('', 0))
    port = s.getsockname()[1]
    return port

def negotiation(req_code, serverSocket):
    #verify req_code from client
    connectionSocket, addr = serverSocket.accept()
    req_code_from_client = connectionSocket.recv(1024).decode()
    if req_code != req_code_from_client:
        result = "0"
        connectionSocket.send(result.encode())
        return -1
    else:
        udp_port = find_open_port(SOCK_DGRAM)
        connectionSocket.send(str(udp_port).encode())

    connectionSocket.close()
    return udp_port

def retrieve(udp_port):
    #establish UDP connection
    serverPort = udp_port
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))

    message, clientAddress = serverSocket.recvfrom(2048)
    msg = str(message.decode())
    if msg == "GET":
        length = len(storage)
        serverSocket.sendto(str(length).encode(), clientAddress)
        for x in storage:
            serverSocket.sendto(x.encode(), clientAddress)

    return serverSocket

def add(udp_port, msg):
    lock = threading.Lock()
    lock.acquire()
    info = "[" + str(udp_port) + "]: " + msg
    storage.insert(0, info)
    q.pop()
    lock.release()

def main():
    #get argument
    req_code = sys.argv[1]

    #create TCP socket
    serverPorttcp = find_open_port(SOCK_STREAM)
    serverSockettcp = socket(AF_INET, SOCK_STREAM)
    serverSockettcp.bind(('', serverPorttcp))
    serverSockettcp.listen(1)
    print("SERVER_PORT=" + str(serverPorttcp))

    while True:
        udp_port = negotiation(req_code, serverSockettcp)
        if udp_port == -1:
            continue
        serverSocketudp = retrieve(udp_port)
        message, clientAddress = serverSocketudp.recvfrom(2048)
        msg = str(message.decode())
        temp = msg
        if msg != "TERMINATE":
            q.append(msg)
            client_thread = threading.Thread(target=add(udp_port, msg))
            client_thread.start()

        if msg == "TERMINATE" and len(q) == 0:
            serverSocketudp.close()
            exit()

if __name__ == "__main__":
    main()