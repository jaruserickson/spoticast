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

    def leave_room(self, addr):
        ''' actually send the leave room request to the server '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.send(('/LEAVE_ROOM').encode('utf-8'))
        sock.send(addr.encode('utf-8'))

        ret_val = sock.recv(1024).decode('utf-8')
        sock.close()

        return ret_val

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
