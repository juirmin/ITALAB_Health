from gtts import gTTS
import os


def tts(mytext='', filename='output.mp3'):
    myobj = gTTS(text=mytext, lang='zh-tw', slow=False)
    myobj.save(filename)
    return True


if __name__ == '__main__':
    soundpath = os.path.join('sound', "finish.mp3")
    print(tts(mytext='良測結束', filename=soundpath))
