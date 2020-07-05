import json
ALL_MSG = 1 #chatmsg,username
USR_JOIN = 2 #
USR_LEFT = 3
USR_REGISTER = 4
USR_LOGIN = 5
ALL_ONLINE_USR = 6
PAI_YI_PAI = 7
ANNOUNCEMENT = 8
DELETE_USR = 9

HOST = '192.168.30.1'
PORT = 8001

def send(msg,conn):
    jmsg = json.dumps(msg)
    conn.send(jmsg.encode("utf-8"))
