# _*_ coding: utf-8 _*_

import socket

host = "192.168.0.30"
port = 50007

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print("Connected...")

while True:
        while True:

                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((host, port))

                key = input('命令を入力>>')

                if key == 'f':
                        print("Sending:","f")
                        dat = 'f'
                        dat = dat.encode()
                        client.send(dat)
                        response = client.recv(4096)
                        print(response)
                        break

                elif key == 'r':
                        print("Sending:","r")
                        dat = 'r'
                        dat = dat.encode()
                        client.send(dat)
                        response = client.recv(4096)
                        print(response)
                        break

                elif key == 'b':
                        print("Sending:","b")
                        dat = 'b'
                        dat = dat.encode()
                        client.send(dat)
                        response = client.recv(4096)
                        print(response)
                        break

                elif key == 'l':
                        print("Sending:","l")
                        dat = 'l'
                        dat = dat.encode()
                        client.send(dat)
                        response = client.recv(4096)
                        print(response)
                        break

                elif key == 's':
                        print("Sending:","s")
                        dat = 's'
                        dat = dat.encode()
                        client.send(dat)
                        response = client.recv(4096)
                        print(response)
                        break
                else:
                        break

                response = client.recv(4096)
                print(response)


