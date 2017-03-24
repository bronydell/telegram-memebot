import numpy as np
import saver
import json

locales = {
    'English': 'bot.json',
    'Русский': 'bot_ru.json'
}


def setLocale(uid, message):
    if message in locales:
        saver.savePref(uid, 'locale', locales[message])


def getLocale(uid):
    return saver.openPref(uid, 'locale', 'bot.json')


def getKeyboard(tag, id):
    settings = getBotSettings(id)
    menu = np.array([])
    for option in settings[tag]['keyboard']:
        if 'admin_only' in option:
            if saver.isAdmin(id) or option['admin_only'] == False:
                menu = np.append(menu, option['text'])
        else:
            menu = np.append(menu, option['text'])
    return np.reshape(menu, (-1, 1))


def getBotSettings(uid):
    with open(getLocale(uid), encoding='UTF-8') as data_file:
        data = json.load(data_file)
    return data
