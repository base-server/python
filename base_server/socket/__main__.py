import sys
import getopt
import signal
from common_library import socket


def args():
    address = ''
    port = 0
    listen_size = 0
    opts, args = getopt.getopt(sys.argv[1:], "ha:p:l",
                               ["address=", "port=", "listen_size="])
    for opt, arg in opts:
        if opt == '-h':
            print('__main__.py --addres <address> --port <port>')
            sys.exit()
        elif opt in ("-a", "--address"):
            address = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-p", "listen_size"):
            listen_size = arg

    return address, int(port), int(listen_size)


def serverJob(client):
    client.send(bytes("greeting\r\n", 'utf-8'))
    data = client.recv(1024).decode('utf-8')
    client.send(bytes("[response] : " + data, 'utf-8'))
    client.close()


def main():
    address, port, listen_size = args()

    server = socket.Server()

    server.start(address=address,
                 port=port,
                 listen_size=listen_size,
                 serverJob=serverJob)

    signal.signal(signal.SIGINT, lambda signum, frame: 0)
    signal.signal(signal.SIGTERM, lambda signum, frame: 0)
    signal.pause()

    server.stop()


if __name__ == '__main__':
    main()
