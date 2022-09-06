from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import sys
from get_user import get_uuid, temperature, oxygen, weight, pressure
from TTS import tts
from readmode import readmode
from fdk300 import FDK300
from fdk400 import FDK400
from m170 import M170
from mtk_a1 import MTKA1
import json
import os
from PyQt5 import QtTest
from pygame import mixer
from net_check import internet_on


class WorkerThread(QObject):
    signalExample = pyqtSignal(str, int)

    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.fdk300 = FDK300()
        self.m170 = M170()
        self.mtka1 = MTKA1()
        self.fdk400 = FDK400()

    @pyqtSlot()
    def run(self):
        while True:
            if self.mode == 'temperature':
                try:
                    data = self.fdk300.get_sensor_data()
                    if data['temperature'] != 0:
                        self.signalExample.emit(json.dumps(data), 200)
                except:
                    pass
            if self.mode == 'oxygen':
                try:
                    data = self.m170.get_sensor_data()
                    print(data)
                    if (data['pulse'] != 0) and (data['pulse'] < 200):
                        self.signalExample.emit(json.dumps(data), 200)
                except:
                    pass
            if self.mode == 'pressure':
                try:
                    data = self.fdk400.get_sensor_data()
                    if data['pressure_S'] != 0:
                        self.signalExample.emit(json.dumps(data), 200)
                except:
                    pass
            if self.mode == 'weight':
                try:
                    data = self.mtka1.get_sensor_data()
                    if data['weight'] != 0:
                        self.signalExample.emit(json.dumps(data), 200)
                except:
                    pass


class MainWindow(QMainWindow):
    def __init__(self, mode):
        QMainWindow.__init__(self)
        self.kdict = {
            'weight': '體重',
            'pressure_S': '收縮壓',
            'pressure_D': '舒張壓',
            'pulse': '脈搏',
            'temperature': '體溫',
            'oxygen': '血氧',
            'pressure': '血壓'
        }
        self.mode = mode
        self.start = False
        self.user_response = {}
        self.setWindowTitle('ITALAB')
        self.worker = WorkerThread(mode=self.mode)
        self.workerThread = QThread()
        self.workerThread.started.connect(self.worker.run)
        self.worker.signalExample.connect(self.signalExample)
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.line.returnPressed.connect(self.login)
        self.login_widget.Title.setText(f"模式：{self.kdict.get(self.mode)}")
        self.central_widget.addWidget(self.login_widget)
        self.logged_in_widget = LoggedWidget(self)
        self.state = 'login'
        self.network_state = False

    def say(self, floder='output.mp3'):
        QtTest.QTest.qWait(0.01)
        mixer.init()
        mixer.music.load(floder)
        mixer.music.play()
        while mixer.music.get_busy():
            continue
        mixer.quit()

    def login(self):
        while self.network_state != True:
            self.network_state = internet_on()
            self.login_widget.Network.setText('沒連接到網路')
            self.login_widget.Network.setStyleSheet("font-size : 20px;text-align: center;color: 'red'")
        self.login_widget.Network.setText('已連接到網路')
        self.login_widget.Network.setStyleSheet("font-size : 20px;text-align: center;color: 'green'")
        try:
            if self.mode in ['oxygen']:
                os.system('sudo systemctl restart bluetooth')
            self.user_response = get_uuid(self.login_widget.line.text())
            if self.user_response['status'] == 200:
                self.start = True
                self.logged_in_widget = LoggedWidget(self)
                self.logged_in_widget.User.setText(f"使用者：{self.user_response['data']['username']}")
                self.central_widget.addWidget(self.logged_in_widget)
                self.central_widget.setCurrentWidget(self.logged_in_widget)
                soundpath = os.path.join("sound", f"{self.user_response['data']['username']}.mp3")
                if f"{self.user_response['data']['username']}.mp3" in os.listdir('sound'):
                    self.say(floder=soundpath)
                elif tts(f"您好，{self.user_response['data']['username']},請開始良測", filename=soundpath):
                    self.say(floder=soundpath)

            else:
                self.login_widget.Label.setText('條碼掃描錯誤\n請重新掃描')
                self.login_widget.line.setText('')
                self.say(os.path.join('sound', 'wrong.mp3'))
                self.login_widget.Label.setText('請掃描條碼')
        except:
            self.login_widget.Label.setText('條碼掃描錯誤\n請重新掃描')
            self.login_widget.line.setText('')
            self.say(os.path.join('sound', 'wrong.mp3'))
            self.login_widget.Label.setText('請掃描條碼')

    def loginout(self, dict1):
        self.start = False
        self.login_widget.line.setText('')
        sw = SensorWidget()
        for k, v in dict1.items():
            if self.kdict.get(k):
                sw.layout.addWidget(sw.La_text(f"{self.kdict.get(k)} : {v}"))
        self.central_widget.addWidget(sw)
        self.login_widget.Label.setText('請掃描條碼')
        self.central_widget.removeWidget(self.logged_in_widget)
        self.central_widget.setCurrentWidget(sw)
        self.say(os.path.join('sound', 'finish.mp3'))
        self.central_widget.setCurrentWidget(self.login_widget)
        self.login_widget.line.setFocus()

    def signalExample(self, text, value):
        if self.start:
            data = json.loads(text)
            uuid = self.user_response['data']['uuid']
            if self.mode == 'temperature':
                if temperature(data, uuid) == 200:
                    self.loginout(data)
            if self.mode == 'oxygen':
                if oxygen(data, uuid) == 200:
                    self.loginout(data)
            if self.mode == 'weight':
                if weight(data, uuid) == 200:
                    self.loginout(data)
            if self.mode == 'pressure':
                if pressure(data, uuid) == 200:
                    self.loginout(data)


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.Network = QLabel(self)
        self.Network.move(30, 60)
        self.Network.resize(200, 30)
        if internet_on():
            self.Network.setText('已連接到網路')
            self.Network.setStyleSheet("font-size : 20px;text-align: center;color: 'green'")
        else:
            self.Network.setText('未連接到網路')
            self.Network.setStyleSheet("font-size : 20px;text-align: center;color: 'red'")

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


class SensorWidget(QWidget):
    def __init__(self, parent=None):
        super(SensorWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def La_text(self, text='text'):
        label = QLabel(text)
        label.setStyleSheet("font-size : 70px;text-align: center")
        return label


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(mode=readmode())
    mainWin.showFullScreen()
    sys.exit(app.exec_())
