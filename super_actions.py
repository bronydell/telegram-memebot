import numpy as np
import saver
import json
import os
import time
from telegram.error import Unauthorized, RetryAfter
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
    try:
        settings = getBotSettings(user)
        uid = update.message.from_user.id
        bot.sendMessage(chat_id=user, text=text)
        time.sleep(0.1)
    except Unauthorized:
        pass
    except RetryAfter as ex:
        time.sleep(ex.retry_after)
        sendMessage(bot, update, user, text)
    except:
        pass

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
