from PyQt5.Qt import QThread, QObject
from PyQt5.QtCore import pyqtSignal
import socket
from Config import *
import json
import hashlib

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendMsg(type, msg, name):
    msg = [type, msg, name]
    jmsg = json.dumps(msg)
    conn.send(jmsg.encode("utf-8"))


def md5_key(arg):
    hash = hashlib.md5()
    hash.update(arg.encode())
    return hash.hexdigest()


class ClientHandler(QThread):
    signal = pyqtSignal(list)

    def __init__(self):
        super(ClientHandler, self).__init__()

    def join(self, name):
        msg = [USR_JOIN, name]
        send(msg, conn)

    def register(self, name, password, nickname):
        password = md5_key(md5_key(password))
        msg = [USR_REGISTER, name, password, nickname]
        send(msg, conn)
        self.issuc = -1
        while self.issuc == -1:
            pass
        return self.issuc

    def login(self, name, password):
        password = md5_key(md5_key(password))
        msg = [USR_LOGIN, name, password]
        send(msg, conn)
        self.issuc = -1
        while self.issuc == -1:
            pass
        return self.issuc

    def pai_yi_pai(self, name, toname):
        # print(name,toname)
        msg = [PAI_YI_PAI, name, toname]
        send(msg, conn)

    def delete_user(self, name):
        print(name)
        msg = [DELETE_USR, name]
        send(msg, conn)

    def announcement(self, text):
        print(text)
        msg = [ANNOUNCEMENT, text]
        send(msg, conn)

    def run(self):
        while True:
            data = conn.recv(1024)
            msg = json.loads(data.decode())
            if msg[0] == USR_REGISTER:
                self.issuc = msg[1]
            if msg[0] == USR_LOGIN:
                self.issuc = msg[1]
            self.signal.emit(msg)
