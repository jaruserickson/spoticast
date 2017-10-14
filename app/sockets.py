''' sockets file '''
import socket
import json

class Sock:
    ''' all the socket connection functions '''
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create_room(self):
        ''' actually send the create room request to the server '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send(('/CREATE_ROOM').encode('utf-8'))
        room_key = sock.recv(1024).decode('utf-8')
        sock.close()

        return room_key

    def join_room(self, addr):
        ''' actually send the join room request to the server '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send(('/JOIN_ROOM').encode('utf-8'))
        sock.send((str(addr)))
        ret_val = sock.recv(1024).decode('utf-8')
        room_data = {}
        if ret_val[0] != '@':
            room_data = json.loads(ret_val)
        else:
            print(ret_val)

        sock.close()
        return room_data

    def send_room(self, addr, room):
        ''' send room data to server room '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send(('/SEND_ROOM').encode('utf-8'))
        sock.send((str(addr)))
        sock.send(json.dumps(room).encode('utf-8'))
        print(sock.recv(1024).decode('utf-8'))
        sock.close()

    def check_room(self, addr):
        ''' get room data '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send(('/GET_ROOM').encode('utf-8'))
        sock.send((str(addr)))
        ret_val = sock.recv(1024).decode('utf-8')
        room_data = {}
        if ret_val[0] != '@':
            room_data = json.loads(ret_val)
        else:
            print(ret_val)

        sock.close()
        return room_data
