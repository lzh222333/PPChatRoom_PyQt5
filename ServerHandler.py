import socketserver
import ServerMain
import json
from Config import *
import requests
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
                    index=msg[1].find("@拍拍")
                    rindex=msg[1].rfind('</p>')
                    print(msg[1])
                    if index!=-1:
                        ServerMain.sendToALL(data,conn)
                        r=requests.get("https://open.drea.cc/bbsapi/chat/get?keyWord="+msg[1][index+2:rindex])
                        msg=[ALL_MSG,r.json()['data']['reply'].replace("Smile","拍拍"),'拍拍']
                        jmsg = json.dumps(msg)
                        data = jmsg.encode("utf-8")
                        ServerMain.sendToALL(data,conn)
                        continue
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
                    #登录成功
                    issuc,admin=ServerMain.user_login(msg[1],msg[2])
                    if issuc:
                        print(msg[1],"登录成功")
                        msg=[USR_LOGIN,1,admin]
                        send(msg,conn)
                    #登录失败
                    else:
                        print(msg[1],"登录失败")
                        msg=[USR_LOGIN,0,0]
                        send(msg,conn)
                    #不广播
                    continue
                elif(msg[0]==ALL_ONLINE_USR):
                    ServerMain.send_online_usr(conn)
                elif(msg[0]==PAI_YI_PAI):
                    pass
                elif(msg[0]==ANNOUNCEMENT):
                    ServerMain.announcement=msg[1]
                    pass
                elif(msg[0]==DELETE_USR):
                    ServerMain.delete_user(msg[1])

                ServerMain.sendToALL(data,conn)
            except ConnectionResetError as e:
                print("error: ",e)
                break
        ServerMain.remove(name)
