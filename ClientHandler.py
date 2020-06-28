from PyQt5.Qt import QThread,QObject
from PyQt5.QtCore import pyqtSignal
import socket
from Config import *
import json

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendMsg(type,msg,name):
    msg=[type,msg,name]
    jmsg = json.dumps(msg)
    conn.send(jmsg.encode("utf-8"))

class ClientHandler(QThread):

    signal = pyqtSignal(list)

    def __init__(self):
        super(ClientHandler,self).__init__()

    def sendName(self,name):
        msg=[USR_JOIN,name]
        jmsg = json.dumps(msg)
        conn.send(jmsg.encode("utf-8"))

    def run(self):
        while True:
            data = conn.recv(1024)
            msg = json.loads(data.decode())
            self.signal.emit(msg)

