import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QTreeWidgetItem, QTreeWidget, QTextEdit, QFontComboBox, QTextBrowser, \
    QPushButton, QWidget, QApplication, QVBoxLayout, QHBoxLayout
from ClientHandler import *

myname = ""


class ClientUI(QWidget):

    def __init__(self):
        super().__init__()
        # self.window = QWidget()
        self.resize(1000, 600)
        self.setWindowTitle("拍一拍聊天室")

        # 聊天窗口
        self.messageBrowser = QTextBrowser()
        # 字体选择
        self.fontCombo = QFontComboBox()

        # 发送按钮
        self.sendButton = QPushButton('发送')
        self.sendButton.clicked.connect(self.sendChatMsg)

        # 发送功能横向布局
        functionboxLayout = QHBoxLayout()
        functionboxLayout.addWidget(self.fontCombo)
        functionboxLayout.addStretch(1)
        functionboxLayout.addWidget(self.sendButton)

        # 输入框
        self.messageEdit = QTextEdit()

        # 左侧竖向布局，三行
        vhoxLayout_left = QVBoxLayout()
        vhoxLayout_left.addWidget(self.messageBrowser)
        vhoxLayout_left.addLayout(functionboxLayout)
        vhoxLayout_left.addWidget(self.messageEdit)

        # 在线用户列表
        self.userView = QTreeWidget()
        self.userView.setHeaderLabels(["用户列表"])
        self.userView_online_node = QTreeWidgetItem(self.userView)
        self.userView_online_node.setText(0, "在线用户")
        # self.addUserNode(self.userView_online_node)

        # 左侧竖向布局，一整块
        vhoxLayout_right = QVBoxLayout()
        vhoxLayout_right.addWidget(self.userView)

        # 最大布局，横向两列
        hboxLayout = QHBoxLayout(self)
        hboxLayout.addLayout(vhoxLayout_left)
        hboxLayout.addLayout(vhoxLayout_right)
        hboxLayout.setStretch(0, 3)
        hboxLayout.setStretch(1, 1)

        self.show()

    def sendChatMsg(self):
        sendMsg(ALL_MSG, self.messageEdit.toPlainText(), myname)
        self.messageEdit.clear()

    def showMsg(self, msg, name):

        if (name != myname):
            self.messageBrowser.append('<p align="left" style="color:blue">' + name+':'+msg + '</p>')
            self.messageBrowser.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            self.messageBrowser.append('<p align="right" style="color:red">' +msg+':我' + '</p>')
            self.messageBrowser.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def addUserNode(self, group, name):
        newUser = QTreeWidgetItem(group)
        newUser.setText(0, name)

    def removeUserNode(self, name):
        print(name)
        findItem = self.userView.findItems(name, Qt.MatchExactly)
        print(findItem)
        if findItem:
            self.userView.removeRow(findItem[0].row())

    def userJoin(self, name):
        self.messageBrowser.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.messageBrowser.append('<div align="center" style="color:grey">系统消息：' + name + '上线了</div>')
        self.addUserNode(self.userView_online_node, name)

    def userLeft(self, name):
        self.messageBrowser.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.messageBrowser.append('<p align="center" style="text-align:center;color:grey">系统消息：' + name + '离开了</p>')
        self.removeUserNode(name)
        print(str(self.messageBrowser.toHtml()))

    def setHandler(self, handler):
        self.handler = handler

    def handler(self, msg):
        type = msg[0]
        if type == ALL_MSG:
            self.showMsg(msg[1], msg[2])
        elif type == USR_JOIN:
            self.userJoin(msg[1])
        elif type == USR_LEFT:
            self.userLeft(msg[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ClientUI()
    conn.connect((HOST, PORT))
    myname = QInputDialog().getText(widget, "注册", "请输入用户名:")
    myname = myname[0]
    handler = ClientHandler()
    handler.signal.connect(widget.handler)
    handler.sendName(myname)
    handler.start()
    sys.exit(app.exec_())
