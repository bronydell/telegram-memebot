import numpy as np
import saver
import json
import os
from telegram.error import Unauthorized
locales = {
    'English': 'bot.json',
    'Русский': 'bot_ru.json'
}


def setLocale(uid, message):
    if message in locales:
        saver.savePref(uid, 'locale', locales[message])


def getLocale(uid):
    return saver.openPref(uid, 'locale', 'bot.json')

def sendMessage(bot, update, user, text=None):
    settings = getBotSettings(user)
    uid = update.message.from_user.id
    message = update.message
    if text is None:
        try:

            if message.reply_to_message:
                bot.forward_message(user, from_chat_id=message.reply_to_message.chat.id,
                                    message_id=message.reply_to_message.message_id)
            if message.photo:
                if message.caption:
                    bot.sendPhoto(chat_id=user, photo=message.photo[-1].file_id, caption=message.caption)
                else:
                    bot.sendPhoto(chat_id=user, photo=message.photo[-1].file_id)
            elif message.text:
                bot.sendMessage(chat_id=user, text=message.text)
            elif message.document:
                if message.caption:
                    bot.sendDocument(chat_id=user, document=message.document.file_id, caption=
                    message.caption)
                else:
                    bot.sendDocument(chat_id=user, document=message.document.file_id)
            elif message.sticker:
                bot.sendSticker(chat_id=user, sticker=message.sticker.file_id)
            elif message.voice:
                if message.caption:
                    bot.sendVoice(chat_id=user, voice=message.voice.file_id, caption=message.caption)
                else:
                    bot.sendVoice(chat_id=user, voice=message.voice.file_id)
            elif message.audio:
                if message.caption:
                    bot.sendAudio(chat_id=user, audio=message.audio.file_id, caption=message.caption)
                else:
                    bot.sendAudio(chat_id=user, audio=message.audio.file_id)
            elif message.video:
                if message.caption:
                    bot.sendVideo(chat_id=user, video=message.video.file_id, caption=message.caption)
                else:
                    bot.sendVideo(chat_id=user, video=message.video.file_id)

        except Unauthorized as ex:
            bot.sendMessage(chat_id=uid, text='Error. Blocked?')

    else:
        bot.sendMessage(chat_id=user, text=text)

def getKeyboard(tag, id):
    settings = getBotSettings(id)
    menu = np.array([])
    for option in settings[tag]['keyboard']:
        if 'admin_only' in option:
            if saver.openPref(id, 'is_admin', False) or option['admin_only'] == False:
                menu = np.append(menu, option['text'])
        elif 'had_image' in option:
            if os.path.exists('images/in_' + str(id) + '.jpg'):
                menu = np.append(menu, option['text'])

        else:
            menu = np.append(menu, option['text'])
    return np.reshape(menu, (-1, 1))


def getBotSettings(uid):
    with open(getLocale(uid), encoding='UTF-8') as data_file:
        data = json.load(data_file)
    return data
