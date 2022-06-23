from gtts import gTTS 
from pydub import AudioSegment
from pydub.playback import play

def tts(mytext):
    try:
        language = 'zh-tw'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("output.mp3") 
        music = AudioSegment.from_mp3('./output.mp3')
        play(music)
    except:
        pass

def playsound(file):
    try:
        music = AudioSegment.from_mp3(f"{file}.mp3")
        play(music)
    except:
        pass

if __name__ == '__main__':
    #tts('請開始良測')
    playsound('wrong')