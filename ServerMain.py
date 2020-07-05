import socket
from ServerHandler import *
from Config import *
import json
import pymysql

active_user={}#用户名_socket连接字典
online_user={}#用户名_昵称字典
announcement="欢迎来到拍一拍聊天室！"
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8001
f=open('config',mode='r')
config=f.readlines()#config是配置文件，自己写
f.close()
db = pymysql.connect(host=config[0].strip(),port=int(config[1].strip()),user=config[2].strip(),passwd=config[3].strip(),db=config[4].strip(),autocommit=True)
cur = db.cursor()

def send_online_usr(conn):
    msg=[ALL_ONLINE_USR,[],announcement,[]]
    for name,nickname in active_user.items():
        msg[1].append(name)
    users=get_all_user()
    for user in users:
        msg[3].append(user[0])
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

def get_all_user():
    cur.execute("SELECT username FROM user_information;")
    return cur.fetchall()

def delete_user(name):
    cur.execute("DELETE FROM user_information WHERE username='"+name+"';")
    if cur.rowcount:
        if name in active_user.keys():
            active_user[name].close()
            remove(name)

def user_register(username,password,nickname):
    cur.execute("SELECT * FROM user_information WHERE username='"+username+"';")
    if cur.rowcount:
        return False
    else:
        return cur.execute("INSERT INTO user_information values('"+username+"','"+password+"','"+nickname+"',0);")

def user_login(username,password):
    print(username,password)
    cur.execute("SELECT admin FROM user_information WHERE username='"+username+"' AND password='"+password+"';")
    if cur.rowcount:
        admin=cur.fetchall()[0]
        return True,admin[0]
    else:
        return False,0

def getNickname(username):
    cur.execute("SELECT nickname FROM user_information WHERE username='"+username+"';")
    uu=cur.fetchall()[0]
    return uu[0]

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer((HOST,PORT), ServerHandler)
    server.serve_forever()
    db.close()

