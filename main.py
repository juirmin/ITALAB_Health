from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import sys
import time
from get_user import get_uuid
from TTS import tts,playsound
from readmode import readmode
from fdk300 import FDK300
from fdk400 import FDK400
from m170 import M170
from mtk_a1 import MTKA1


class WorkerThread(QObject):
    signalExample = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        while True:
            self.signalExample.emit("leet", 1337)
            time.sleep(0.001)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mode = readmode()
        self.start = False
        self.user_response = {}
        self.setWindowTitle('ITALAB')
        self.worker = WorkerThread()
        self.workerThread = QThread()
        self.workerThread.started.connect(self.worker.run)
        self.worker.signalExample.connect(self.signalExample)
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.line.returnPressed.connect(self.login)
        self.login_widget.Title.setText(self.mode)
        self.central_widget.addWidget(self.login_widget)

    def login(self):
        try:
            self.user_response = get_uuid(self.login_widget.line.text())
            if self.user_response['status'] == 200:
                logged_in_widget = LoggedWidget(self)
                logged_in_widget.User.setText(f"使用者：{self.user_response['data']['username']}")
                logged_in_widget.birthday.setText(f"生日：{self.user_response['data']['birthday']}")
                self.central_widget.addWidget(logged_in_widget)
                self.central_widget.setCurrentWidget(logged_in_widget)
                tts('請開始良測')
                time.sleep(0.5)
                self.start = True
            else:
                self.login_widget.Label.setText('條碼掃描錯誤\n請重新掃描')
                self.login_widget.line.setText('')
                playsound("wrong")
        except:
            self.login_widget.Label.setText('條碼掃描錯誤\n請重新掃描')
            self.login_widget.line.setText('')
            playsound("wrong")

    def loginout(self):
        print(self.login_widget.line.text())
        self.login_widget.line.setText('')
        self.central_widget.addWidget(self.login_widget)
        self.central_widget.setCurrentWidget(self.login_widget)
    
    def signalExample(self, text):
        if self.start:
            if self.mode=='temperature':
                try:
                    fdk300 = FDK300()
                    _temp = fdk300.get_sensor_data()
                    sensor_data = {'temperature': _temp['temperature']}
                    print(sensor_data["temperature"])
                    if sensor_data["temperature"]!=0:
                        print('break')
                except:
                    pass

class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.Title = QLabel(self)
        self.Title.move(30, 30)
        self.Title.resize(200, 30)
        self.Title.setStyleSheet("font-size : 20px;text-align: center")
        self.Label = QLabel(self)
        self.Label.setText('請掃描條碼')
        self.Label.setAlignment(Qt.AlignCenter)
        self.Label.setStyleSheet("font-size : 100px;border : 2px solid black;text-align: center")
        self.line = QLineEdit(self)
        self.line.move(0, 0)
        self.line.resize(0, 0)
        layout.addWidget(self.Label)
        self.setLayout(layout)
        

class LoggedWidget(QWidget):
    def __init__(self, parent=None):
        super(LoggedWidget, self).__init__(parent)
        layout = QVBoxLayout()

        self.User = QLabel('')
        self.birthday = QLabel('')
        self.Label = QLabel('請開始量測')
        self.User.setAlignment(Qt.AlignCenter)
        self.birthday.setAlignment(Qt.AlignCenter)
        self.Label.setAlignment(Qt.AlignCenter)
        self.User.setStyleSheet("font-size : 70px;text-align: center")
        self.birthday.setStyleSheet("font-size : 70px;text-align: center")
        self.Label.setStyleSheet("color :'blue';font-size : 50px;text-align: center;margin-top:100px")
        layout.addWidget(self.User)
        layout.addWidget(self.birthday)
        layout.addWidget(self.Label)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.showFullScreen()
    sys.exit(app.exec_())
