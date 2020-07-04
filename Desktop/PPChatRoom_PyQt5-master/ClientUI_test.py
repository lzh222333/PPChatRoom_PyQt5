import sys
import codecs
from PyQt5.QtCore import Qt,pyqtSlot,QDateTime, QCoreApplication, QSize, QFileInfo
from PyQt5.QtGui import QColor, QTextCharFormat,QTextCursor, QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QMessageBox, QLabel, QLineEdit, QInputDialog, QTreeWidgetItem, QTreeWidget, QTextEdit, QFontComboBox, QTextBrowser, \
    QPushButton, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QComboBox, QToolButton, QColorDialog, QFileDialog
from ClientHandler import *

myname = ""
handler = ClientHandler()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登陆界面")
        self.resize(550, 225)
        self.Co_Width = 40
        self.Co_Heigth = 20
        self.setup_ui()
        self.lab_nickname.setVisible(False)
        self.Lin_nickname.setVisible(False)
        #self.handler = handler

    def setup_ui(self):
        self.lab_usrname = QLabel("帐户:", self)  # 帐户标签
        self.Lin_usrname = QLineEdit(self)  # 帐户录入框
        self.lab_pword = QLabel("密码:", self)  # 密码标签
        self.Lin_pword = QLineEdit(self)  # 密码录入框
        self.Lin_pword.setEchoMode(QLineEdit.Password)  # 设置密文显示
        self.lab_nickname = QLabel("昵称:", self)  # 昵称标签
        self.Lin_nickname = QLineEdit(self)  # 昵称录入框
        self.Pu_login = QPushButton( "登录", self)  # 登陆按钮
        self.Pu_login.clicked.connect(self.login)
        self.Pu_register = QPushButton("注册", self)  # 登陆按钮
        self.Pu_register.clicked.connect(self.register)

    def resizeEvent(self, evt):  # 重新设置控件座标事件
        # 帐户标签
        self.lab_usrname.resize(self.Co_Width, self.Co_Heigth)
        self.lab_usrname.move(self.width() / 3, self.height() / 5)
        # 帐户录入框
        self.Lin_usrname.move(self.lab_usrname.x() + self.lab_usrname.width(), self.lab_usrname.y())
        # 密码标签
        self.lab_pword.resize(self.Co_Width, self.Co_Heigth)
        self.lab_pword.move(self.lab_usrname.x(), self.lab_usrname.y() + self.lab_usrname.height() * 2)
        # 密码录入框
        self.Lin_pword.move(self.lab_pword.x() + self.lab_pword.width(), self.lab_pword.y())
        # # 昵称标签
        self.lab_nickname.resize(self.Co_Width, self.Co_Heigth)
        self.lab_nickname.move(self.lab_usrname.x(), self.lab_usrname.y() + self.lab_usrname.height() * 4)
        # 昵称录入框
        self.Lin_nickname.move(self.lab_nickname.x() + self.lab_nickname.width(), self.lab_nickname.y())
        # 登陆按钮
        self.Pu_login.move(self.Lin_nickname.x() - self.Lin_nickname.width() / 2, self.lab_nickname.y() + self.lab_nickname.width())
        self.Pu_register.move(self.Lin_nickname.x() + self.Lin_nickname.width(), self.lab_nickname.y() + self.lab_nickname.width())

    def login(self):
        global myname
        name = self.Lin_usrname.text()
        password = self.Lin_pword.text()
        if handler.login(name,password):
            handler.join(name)
            myname=name
            self.close()
        else:
            QMessageBox.warning(self, "警告", "登录失败！", QMessageBox.Ok)
            print("登录失败！")

    def register(self):
        global myname
        name = self.Lin_usrname.text()
        password = self.Lin_pword.text()
        #nickname =  self.Lin_nickname.text()
        if handler.register(name,password,":"):
            handler.join(name)
            myname=name
            self.close()
        else:
            QMessageBox.warning(self, "警告", "注册失败！", QMessageBox.Ok)
            print("注册失败！")

class ClientUI(QWidget):

    def __init__(self):
        super().__init__()
        # self.window = QWidget()
        self.resize(1000, 600)
        self.setWindowTitle("拍一拍聊天室")

        # 聊天窗口
        self.messageBrowser = QTextBrowser()

        # 字体选择
        self.fontComboBox = QFontComboBox()
        self.fontComboBox.setObjectName("fontComboBox")
        self.fontComboBox.currentFontChanged.connect(self.on_fontComboBox_currentFontChanged)

        # 字体大小
        self.sizeComboBox = QComboBox()
        self.sizeComboBox.setObjectName("SizeComboBox")
        self.sizeComboBox.setCurrentIndex(0)
        for i in range(31):
            self.sizeComboBox.addItem("")
        _translate = QCoreApplication.translate
        self.sizeComboBox.setCurrentText(_translate("Widget", "10"))
        for i in range(31):
            self.sizeComboBox.setItemText(i, _translate("Widget", str(i+10)))
        self.sizeComboBox.currentIndexChanged.connect(self.on_SizeComboBox_currentIndexChanged)

        # 加粗
        self.boldToolBtn = QToolButton()
        self.boldToolBtn.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        root = QFileInfo(__file__).absolutePath()   # 获取根目录
        icon.addPixmap(QPixmap(root+"/image/bold.png"), QIcon.Normal, QIcon.Off)
        self.boldToolBtn.setIcon(icon)
        self.boldToolBtn.setIconSize(QSize(22, 22))
        self.boldToolBtn.setCheckable(True)
        self.boldToolBtn.setAutoRaise(True)
        self.boldToolBtn.setObjectName("boldToolBtn")
        self.boldToolBtn.setToolTip(_translate("Widget", "加粗"))
        self.boldToolBtn.setText(_translate("Widget", "..."))
        self.boldToolBtn.clicked.connect(self.on_boldToolBtn_clicked)

        # 斜体
        self.italicToolBtn = QToolButton()
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(root+"/image/italic.png"), QIcon.Normal, QIcon.Off)
        self.italicToolBtn.setIcon(icon1)
        self.italicToolBtn.setIconSize(QSize(22, 22))
        self.italicToolBtn.setCheckable(True)
        self.italicToolBtn.setAutoRaise(True)
        self.italicToolBtn.setObjectName("italicToolBtn")
        self.italicToolBtn.setToolTip(_translate("Widget", "倾斜"))
        self.italicToolBtn.setText(_translate("Widget", "..."))
        self.italicToolBtn.clicked.connect(self.on_italicToolBtn_clicked)

        # 下划线
        self.underlineToolBtn = QToolButton()
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(root+"/image/under.png"), QIcon.Normal, QIcon.Off)
        self.underlineToolBtn.setIcon(icon2)
        self.underlineToolBtn.setIconSize(QSize(22, 22))
        self.underlineToolBtn.setCheckable(True)
        self.underlineToolBtn.setAutoRaise(True)
        self.underlineToolBtn.setObjectName("underlineToolBtn")
        self.underlineToolBtn.setToolTip(_translate("Widget", "下划线"))
        self.underlineToolBtn.setText(_translate("Widget", "..."))
        self.underlineToolBtn.clicked.connect(self.on_underlineToolBtn_clicked)

        # 颜色
        self.colorToolBtn = QToolButton()
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(root+"/image/color.png"), QIcon.Normal, QIcon.Off)
        self.colorToolBtn.setIcon(icon3)
        self.colorToolBtn.setIconSize(QSize(22, 22))
        self.colorToolBtn.setAutoRaise(True)
        self.colorToolBtn.setObjectName("colorToolBtn")
        self.colorToolBtn.setToolTip(_translate("Widget", "更改字体颜色"))
        self.colorToolBtn.setText(_translate("Widget", "..."))
        self.colorToolBtn.clicked.connect(self.on_colorToolBtn_clicked)

        # 聊天记录
        self.saveToolBtn = QToolButton()
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(root+"/image/save.png"), QIcon.Normal, QIcon.Off)
        self.saveToolBtn.setIcon(icon4)
        self.saveToolBtn.setIconSize(QSize(22, 22))
        self.saveToolBtn.setAutoRaise(True)
        self.saveToolBtn.setObjectName("saveToolBtn")
        self.saveToolBtn.setToolTip(_translate("Widget", "保存聊天记录"))
        self.saveToolBtn.setText(_translate("Widget", "..."))
        self.saveToolBtn.clicked.connect(self.on_saveToolBtn_clicked)

        self.clearToolBtn = QToolButton()
        icon5 = QIcon()
        icon5.addPixmap(QPixmap(root+"/image/clear.png"), QIcon.Normal, QIcon.Off)
        self.clearToolBtn.setIcon(icon5)
        self.clearToolBtn.setIconSize(QSize(22, 22))
        self.clearToolBtn.setAutoRaise(True)
        self.clearToolBtn.setObjectName("clearToolBtn")
        self.clearToolBtn.setToolTip(_translate("Widget", "清空聊天记录"))
        self.clearToolBtn.setText(_translate("Widget", "..."))
        self.clearToolBtn.clicked.connect(self.on_clearToolBtn_clicked)

        # 发送按钮
        self.sendButton = QPushButton('发送')
        self.sendButton.clicked.connect(self.sendChatMsg)

        # 发送功能横向布局
        functionboxLayout = QHBoxLayout()
        functionboxLayout.addWidget(self.fontComboBox)
        functionboxLayout.addWidget(self.sizeComboBox)
        functionboxLayout.addWidget(self.boldToolBtn)
        functionboxLayout.addWidget(self.italicToolBtn)
        functionboxLayout.addWidget(self.underlineToolBtn)
        functionboxLayout.addWidget(self.colorToolBtn)
        functionboxLayout.addWidget(self.saveToolBtn)
        functionboxLayout.addWidget(self.clearToolBtn)
        functionboxLayout.addStretch(1)
        functionboxLayout.addWidget(self.sendButton)

        # 输入框
        self.messageEdit = QTextEdit()

        # 左侧竖向布局，三行
        vhoxLayout_left = QVBoxLayout()
        vhoxLayout_left.addWidget(self.messageBrowser)
        vhoxLayout_left.addLayout(functionboxLayout)
        vhoxLayout_left.addWidget(self.messageEdit)
        vhoxLayout_left.setStretch(0, 4)
        vhoxLayout_left.setStretch(1, 1)
        vhoxLayout_left.setStretch(2, 2)

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

    def mergeFormatDocumentOrSelection(self, format):

        cursor = self.messageEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
        cursor.mergeCharFormat(format)
        self.messageEdit.mergeCurrentCharFormat(format)

    def on_fontComboBox_currentFontChanged(self, p0):
        fmt = QTextCharFormat()
        fmt.setFont(p0)
        #fmt.setFontFamily(p0)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageEdit.setFocus()

    # 字体大小
    def on_SizeComboBox_currentIndexChanged(self, p0):
        fmt = QTextCharFormat()
        p0 += 10
        fmt.setFontPointSize(p0)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageEdit.setFocus()

    def on_boldToolBtn_clicked(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontWeight(checked and QFont.Bold or QFont.Normal)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageEdit.setFocus()

    def on_italicToolBtn_clicked(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageEdit.setFocus()

    def on_underlineToolBtn_clicked(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageEdit.setFocus()

    def on_colorToolBtn_clicked(self):
        col = QColorDialog.getColor(self.messageEdit.textColor(), self)
        if not col.isValid():
            return
        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatDocumentOrSelection(fmt)
        self.messageEdit.setFocus()

    def on_saveToolBtn_clicked(self):
        print(self.messageBrowser.document().isEmpty())
        if self.messageBrowser.document().isEmpty():
            QMessageBox.warning(self, "警告", "聊天记录为空,无法保存!", QMessageBox.Ok)
        else:
            fileName = QFileDialog.getSaveFileName(self, "保存聊天记录", "./聊天记录",
                                                   ("ODT files (*.odt);;HTML-Files (*.htm *.html)"))

            if fileName[0]:
                if self.saveFile(fileName[0]):
                    QMessageBox.information(self, "聊天记录保存", "保存成功！")


    def saveFile(self, fileName):

        SuffixFileName = fileName.split(".")[1]
        if SuffixFileName in ("htm", "html"):
            content = self.messageBrowser.toHtml()
        else:
            content = self.messageBrowser.toPlainText()
        try:
            with codecs.open(fileName, 'w', encoding="gbk") as f:
                f.write(content)
            return True
        except IOError:
            QMessageBox.critical(self, "保存错误", "聊天记录保存失败！")
            return False


    def on_clearToolBtn_clicked(self):
        self.messageBrowser.clear()


    def getMessage(self):
        msg = self.messageEdit.toHtml()
        self.messageEdit.clear()
        self.messageEdit.setFocus()
        return msg

    def sendChatMsg(self):
        sendMsg(ALL_MSG, self.getMessage(), myname)
        self.messageEdit.clear()

    def showMsg(self, msg, name):
        time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        if (name != myname):
            self.messageBrowser.setTextColor(Qt.blue)
            self.messageBrowser.append("[" + name + "] " + time)
            self.messageBrowser.append(msg)
        else:
            self.messageBrowser.setTextColor(Qt.red)
            self.messageBrowser.append("[我] " + time)
            self.messageBrowser.append(msg)

    def addUserNode(self, group, name):
        self.userView.expandAll()
        newUser = QTreeWidgetItem(group)
        newUser.setText(0, name)
        if(name==myname):
            newUser.setBackground(0,QColor('#ABAEEE'))

    def removeUserNode(self, name):
        n = self.userView_online_node.childCount()
        for i in range(n):
            if self.userView_online_node.child(i).text(0)==name:
                self.userView_online_node.removeChild(self.userView_online_node.child(i))
                break

    def userJoin(self, name):
        self.messageBrowser.setTextColor(Qt.gray)
        self.messageBrowser.append('系统消息：' + name + '上线了')

        #self.messageBrowser.append('<div align="center" style="color:grey">系统消息：' + name + '上线了</div>')
        self.addUserNode(self.userView_online_node, name)

    def userLeft(self, name):
        self.messageBrowser.setTextColor(Qt.gray)
        self.messageBrowser.append('系统消息：' + name + '离开了')

        #<p align="center" style="text-align:center;color:grey">
        self.removeUserNode(name)
        #print(str(self.messageBrowser.toHtml()))

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
        elif type == ALL_ONLINE_USR:
            for i in msg[1]:
                self.userJoin(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ClientUI()
    conn.connect((HOST, PORT))
    loginwindow=LoginWindow()
    loginwindow.show()
    handler.signal.connect(widget.handler)
    handler.start()
    sys.exit(app.exec_())
