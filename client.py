from socket import *
import sys
import subprocess


def negotiation(server_address, n_port, req_code):
    #create a TCP socket and connect to server
    serverNametcp = server_address
    serverPorttcp = int(n_port)
    clientSockettcp = socket(AF_INET, SOCK_STREAM)
    clientSockettcp.connect((serverNametcp, serverPorttcp))

    #send req_code to server
    clientSockettcp.send(req_code.encode())

    #verify req_code
    result = clientSockettcp.recv(1024).decode()
    if result == "0":
        print("Invalid req_code.")
        exit()
        
    port_number = result
    
    clientSockettcp.close()
    return port_number

def retrieve_add(udp_port, server_address, msg):
    #establish UDP connection
    serverNameudp = str(server_address)
    serverPortudp = int(udp_port)
    clientSocketudp = socket(AF_INET, SOCK_DGRAM)

    #send GET and print messages
    message = "GET"
    clientSocketudp.sendto(message.encode(), (serverNameudp, serverPortudp))
    length, server_address = clientSocketudp.recvfrom(2048)
    for x in range(int(length)):
        messages, server_address = clientSocketudp.recvfrom(2048)
        print(messages)
    print("")


    #send text message
    clientSocketudp.sendto(msg.encode(), (serverNameudp, serverPortudp))


    
def main():
    #get arguments
    server_address = sys.argv[1]
    n_port = sys.argv[2]
    req_code = sys.argv[3]
    msg = sys.argv[4]

    #negotiation
    udp_port = negotiation(server_address, n_port, req_code)

    #retrieve and add message
    retrieve_add(udp_port, server_address, msg)

    #wait for keyboard input to exit
    print("Press any key to exit.")
    subprocess.call("read -n1 -s", shell=True, executable="/bin/bash")


if __name__ == "__main__":
    main()