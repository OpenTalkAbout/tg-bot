import os
import random
from datetime import datetime
from re import I
import requests
import pyowm
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from moviepy.editor import *
from hello.on_event.get_text import init


def cm_start(update, context):
    update.message.reply_text(
        'Привет {}, ты написал мне /start'.format(update.message.from_user.first_name))


def cm_hello(update, context):
    update.message.reply_text(
        'Привет {}'.format(update.message.from_user.first_name))


def cm_random(update, context):
    update.message.reply_text(
        'Рандом число = {}'.format(random.randint(0, 10)))


def cm_date_time(update, context):
    now_date = str(datetime.now().strftime("%d.%m.%y"))
    hours = int(str(datetime.now().strftime("%H")))
    hours += 3
    now_time = str(datetime.now().strftime(":%M:%S.%f"))
    update.message.reply_text(
        'Сегодняшнее дата {} и время {}{}'.format(now_date, str(hours), now_time))


def cm_coin(update, context):
    bd_coin = ["Орел", "Решка"]
    update.message.reply_text(
        '{}'.format(bd_coin[random.randint(0, (len(bd_coin)-1))]))


def cm_dog(update, context):
    update.message.reply_text(requests.get('https://random.dog/woof.json').json()['url'])


def cm_cat(update, context):
    update.message.reply_text(requests.get('http://thecatapi.com/api/images/get').url)


def cm_weather(update, context):
    sf = OWM.weather_at_place('Минск')
    weather = sf.get_weather()
    context.bot.send_message(
        update.effective_chat.id, 'Погода в городе Минск: {}°C'.format(str(weather.get_temperature('celsius')['temp'])))


def cm_version(update, context):
    update.message.reply_text('v1.0')


def cm_speak(update, context):
    tts = gTTS(text=update.message.text[7:], lang='ru')
    tts.save("speak.mp3")
    context.bot.send_audio(update.effective_chat.id,
                           open(str(os.path.abspath('speak.mp3')), 'rb'))
    os.remove('speak.mp3')


def cm_text(update, context):
    init(update, context, OWM)


def speech_to_text(update: Update, context: CallbackContext):
    try:
        bot = context.bot
        file = bot.getFile(update.message.voice.file_id)
        file.download('voice.ogg')
        m4a_audio = AudioSegment.from_file("voice.ogg", format="ogg")
        m4a_audio.export("voice.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("voice.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="ru")
            update.message.reply_text(text)

        os.remove('voice.ogg')
        os.remove('voice.wav')
    except:
        os.remove('voice.ogg')
        os.remove('voice.wav')


def video_to_text(update: Update, context: CallbackContext):
    try:
        bot = context.bot
        file = bot.getFile(update.message.video.file_id)
        file.download('video.mp4')
        video = VideoFileClip("video.mp4")
        video.audio.write_audiofile("voice.mp3")
        m4a_audio = AudioSegment.from_file("voice.mp3", format="mp3")
        m4a_audio.export("voice.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("voice.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="ru")
            update.message.reply_text(text)

        os.remove('video.mp4')
        os.remove('voice.mp3')
        os.remove('voice.wav')
    except:
        os.remove('video.mp4')
        os.remove('voice.mp3')
        os.remove('voice.wav')


def video_note_to_text(update: Update, context: CallbackContext):
    try:
        bot = context.bot
        file = bot.getFile(update.message.video_note.file_id)
        file.download('video.mp4')
        video = VideoFileClip("video.mp4")
        video.audio.write_audiofile("voice.mp3")
        m4a_audio = AudioSegment.from_file("voice.mp3", format="mp3")
        m4a_audio.export("voice.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("voice.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="ru")
            update.message.reply_text(text)

        os.remove('video.mp4')
        os.remove('voice.mp3')
        os.remove('voice.wav')
    except:
        os.remove('video.mp4')
        os.remove('voice.mp3')
        os.remove('voice.wav')


def cm_voice(update, context):
    speech_to_text(update, context)


def cm_video(update, context):
    video_to_text(update, context)


def cm_video_note(update, context):
    video_note_to_text(update, context)
    

def index():
    print('Server is worked')
    

TOKEN = os.environ.get('TG_BOT_TOKEN')
PORT = os.environ.get('PORT')
OWM = pyowm.OWM(os.environ.get('OWM_TOKEN'))


updater = Updater(TOKEN, use_context=True)

dp = updater
dp.dispatcher.add_handler(CommandHandler('start', cm_start))
dp.dispatcher.add_handler(CommandHandler('hello', cm_hello))
dp.dispatcher.add_handler(CommandHandler('random', cm_random))
dp.dispatcher.add_handler(CommandHandler('datetime', cm_date_time))
dp.dispatcher.add_handler(CommandHandler('coin', cm_coin))
dp.dispatcher.add_handler(CommandHandler('dog', cm_dog))
dp.dispatcher.add_handler(CommandHandler('cat', cm_cat))
dp.dispatcher.add_handler(CommandHandler('weather', cm_weather))
dp.dispatcher.add_handler(CommandHandler('version', cm_version))
dp.dispatcher.add_handler(CommandHandler('speak', cm_speak))
dp.dispatcher.add_handler(MessageHandler(Filters.text, cm_text))
dp.dispatcher.add_handler(MessageHandler(Filters.voice, cm_voice))
dp.dispatcher.add_handler(MessageHandler(Filters.video, cm_video))
dp.dispatcher.add_handler(MessageHandler(Filters.video_note, cm_video_note))
dp.start_polling()