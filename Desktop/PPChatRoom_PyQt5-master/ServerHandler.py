import socketserver
import ServerMain
import json
from Config import *
class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        conn = self.request
        addr = self.client_address
        name = ""
        ServerMain.send_online_usr(conn)
        while True:
            try:
                data = conn.recv(1024)
                msg = json.loads(data.decode())
                #用户加入
                if(msg[0]==USR_JOIN):
                    ServerMain.join(msg[1],conn)
                    name=msg[1]
                #广播消息
                elif(msg[0]==ALL_MSG):
                    pass
                #用户注册
                elif(msg[0]==USR_REGISTER):
                    #注册成功
                    if ServerMain.user_register(msg[1],msg[2],msg[3]):
                        print(msg[1],"注册成功")
                        msg=[USR_REGISTER,1]
                        send(msg,conn)
                    #注册失败
                    else:
                        print(msg[1],"注册失败")
                        msg=[USR_REGISTER,0]
                        send(msg,conn)
                    #不广播
                    continue
                #用户登录
                elif(msg[0]==USR_LOGIN):
                    #注册成功
                    if ServerMain.user_login(msg[1],msg[2]):
                        print(msg[1],"登录成功")
                        msg=[USR_LOGIN,1]
                        send(msg,conn)
                    #注册失败
                    else:
                        print(msg[1],"登录失败")
                        msg=[USR_LOGIN,0]
                        send(msg,conn)
                    #不广播
                    continue
                elif(msg[0]==ALL_ONLINE_USR):
                    ServerMain.send_online_usr(conn)

                ServerMain.sendToALL(data,conn)
            except ConnectionResetError as e:
                print("error: ",e)
                break
        ServerMain.remove(name)
