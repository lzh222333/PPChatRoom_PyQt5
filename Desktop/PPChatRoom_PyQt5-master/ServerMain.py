import socket
from ServerHandler import *
from Config import *
import json
import pymysql

active_user={}#用户名_socket连接字典
online_user={}#用户名_昵称字典
HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 8001
f=open('config',mode='r')
config=f.readlines()#config是配置文件，自己写
f.close()
db = pymysql.connect(host=config[0].strip(),port=int(config[1].strip()),user=config[2].strip(),passwd=config[3].strip(),db=config[4].strip(),autocommit=True)
cur = db.cursor()

def send_online_usr(conn):
    msg=[ALL_ONLINE_USR,[]]
    for name,nickname in active_user.items():
        msg[1].append(name)
    print(msg)
    send(msg,conn)

def join(name,conn):
    if name not in active_user:
        active_user[name]=conn
        online_user[name]=getNickname(name)
    print("当前在线",len(active_user))

def sendToALL(data,from_conn):
    for conn in active_user.values():
        conn.sendall(data)

def remove(name):
    active_user.pop(name)
    online_user.pop(name)
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
        return cur.execute("INSERT INTO user_information values('"+username+"','"+password+"','"+nickname+"');")

def user_login(username,password):
    print(username,password)
    cur.execute("SELECT * FROM user_information WHERE username='"+username+"' AND password='"+password+"';")
    if cur.rowcount:
        return True
    else:
        return False

def getNickname(username):
    cur.execute("SELECT nickname FROM user_information WHERE username='"+username+"';")
    uu=cur.fetchall()[0]
    return uu[0]

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer((HOST,PORT), ServerHandler)
    server.serve_forever()
    db.close()

