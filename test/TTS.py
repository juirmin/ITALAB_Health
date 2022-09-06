from gtts import gTTS
def tts(mytext='', filename='output.mp3'):
    myobj = gTTS(text=mytext, lang='zh-tw', slow=False)
    myobj.save(filename)
    return True


if __name__ == '__main__':
    print(tts(mytext='任鄭成功'))
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtTextToSpeech import QTextToSpeech
# import sys
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#
#         centralWidget = QWidget()
#         self.setCentralWidget(centralWidget)
#         layout = QFormLayout(centralWidget)
#
#         textLayout = QHBoxLayout()
#         self.text = QLineEdit('Hello, PySide2')
#         self.text.setClearButtonEnabled(True)
#         textLayout.addWidget(self.text)
#         self.sayButton = QPushButton('Say')
#         textLayout.addWidget(self.sayButton)
#         self.text.returnPressed.connect(self.sayButton.animateClick)
#         self.sayButton.clicked.connect(self.say)
#         layout.addRow('Text:', textLayout)
#
#         self.voiceCombo = QComboBox()
#         layout.addRow('Voice:', self.voiceCombo)
#
#         self.volumeSlider = QSlider(Qt.Horizontal)
#         self.volumeSlider.setMinimum(0)
#         self.volumeSlider.setMaximum(100)
#         self.volumeSlider.setValue(100)
#         layout.addRow('Volume:', self.volumeSlider)
#
#         self.engine = None
#         engineNames = QTextToSpeech.availableEngines()
#         if len(engineNames) > 0:
#             engineName = engineNames[0]
#             self.engine = QTextToSpeech(engineName)
#             self.engine.stateChanged.connect(self.stateChanged)
#             self.setWindowTitle('QTextToSpeech Example ({})'.format(engineName))
#             self.voices = []
#             for voice in self.engine.availableVoices():
#                 self.voices.append(voice)
#                 self.voiceCombo.addItem(voice.name())
#         else:
#             self.setWindowTitle('QTextToSpeech Example (no engines available)')
#             self.sayButton.setEnabled(False)
#
#     def say(self):
#         self.sayButton.setEnabled(False)
#         self.engine.setVoice(self.voices[self.voiceCombo.currentIndex()])
#         self.engine.setVolume(float(self.volumeSlider.value()) / 100)
#         self.engine.say(self.text.text())
#
#     def stateChanged(self, state):
#         if (state == QTextToSpeech.State.Ready):
#             self.sayButton.setEnabled(True)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWin = MainWindow()
#     mainWin.show()
#     sys.exit(app.exec_())
