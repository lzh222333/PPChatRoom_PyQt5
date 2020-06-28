import socket
from ServerHandler import *
from Config import *
import json
import pymysql

active_user={}#用户字典
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8001
f=open('config',mode='r')
config=f.readlines()#config是配置文件，自己写
f.close()
db = pymysql.connect(host=config[0].strip(),port=int(config[1].strip()),user=config[2].strip(),passwd=config[3].strip(),db=config[4].strip(),autocommit=True)
cur = db.cursor()

def join(name,conn):
    if name not in active_user:
        active_user[name]=conn
    print("当前在线",len(active_user))

def sendToALL(data,from_conn):
    for conn in active_user.values():
        conn.sendall(data)

def remove(name):
    active_user.pop(name)
    print("当前在线",len(active_user))
    msg=[USR_LEFT,name]
    jmsg = json.dumps(msg)
    sendToALL(jmsg.encode('utf-8'),name)

def active_user_size():
    return len(active_user)

def user_register(username,password,nickname):
    cur.execute("SELECT * FROM user_information WHERE username='"+username+"';")
    if cur.rowcount:
        return False
    else:
        cur.execute("INSERT INTO user_information values('"+username+"','"+password+"','"+nickname+"');")

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer((HOST,PORT), ServerHandler)
    server.serve_forever()
    db.close()

