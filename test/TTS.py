# from gtts import gTTS
#
# def tts(mytext):
#     try:
#         language = 'zh-tw'
#         myobj = gTTS(text=mytext, lang='zh-tw', slow=False)
#
#         myobj.save("output.mp3")
#     except:
#         raise
#
# if __name__ == '__main__':
#     tts('請開始良測')
#
#     # playsound('wrong')
import pyttsx3


def onStart(name):
   print('starting', name)
def onWord(name, location, length):
   print ('word', name, location, length)
def onEnd(name, completed):
   print('finishing', name, completed)


engine = pyttsx3.init()

voices = engine.getProperty('voices')
print(voices)
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('認證成功.')
engine.runAndWait()

