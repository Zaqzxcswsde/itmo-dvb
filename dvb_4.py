import json
import pyttsx3, vosk, pyaudio, requests

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    # print(voice.name)
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        tts.setProperty('voice', voice.id)

model = vosk.Model('./vosk-model-small-ru-0.4/')
record = vosk.KaldiRecognizer(model, 16000)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()

# class jokeClass:
#     def __init__(self):
#         self.text = None
#         self.type = None
#         self.category = None

#     def get(self):
#         data = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode').json()
#         self.type = data['type']
#         self.text = data['joke'] if data['type']=='single' else data['setup']+'\n'+data['delivery']
#         self.category = data['category']

joke = None

def parse(text):
    global joke

    if text not in ['создать','тип','прочесть','категория','сохранить','выход']:
        print('unrecognized command:',text)
        return

    if text == 'создать':
        data = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode').json()
        joke = {'type':data['type'],
                'text': data['joke'] if data['type']=='single' else data['setup']+'\n'+data['delivery'],
                'category': data['category']}
        print(joke)
        return
    
    if text == 'выход':
        quit()
    
    if not joke:
        print('no joke stored')
        return
    if text == 'тип':
        print(joke['type'])
    elif text == 'прочесть':
        speak(joke['text'])
    elif text == 'категория':
        print(joke['category'])
    elif text == 'сохранить':
        with open('jokes.txt','at') as f:
            f.write(joke['text']+'\n---\n')
            print('saved')


print('start')
for text in listen():
    parse(text)


