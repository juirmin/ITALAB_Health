from gtts import gTTS
def tts(mytext='', filename='output.mp3'):
    myobj = gTTS(text=mytext, lang='zh-tw', slow=False)
    myobj.save(filename)
    return True


if __name__ == '__main__':
    print(tts(mytext='任鄭成功'))