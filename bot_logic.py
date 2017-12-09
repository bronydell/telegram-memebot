#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, telegram
from telegram.ext import Updater, CommandHandler
import saver, generator
import numpy as np
import super_actions as actions
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

with open('botan.config', 'r') as myfile:  # You must put key for your bot in botan.config!!! IMPORTANT!!!!
    botan_token = myfile.read().replace('\n', '')


def topTextView(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Top'
    saver.savePref(uid, 'Action', 'top')
    saver.savePref(uid, 'Top', '')
    bot.sendMessage(update.message.chat_id,
                    text=settings['top']['message'],
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('top', uid)))


def capsView(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Caps settings'
    saver.savePref(uid, 'Action', 'caps')
    bot.sendMessage(update.message.chat_id,
                    text=settings['caps']['message'],
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('caps', uid)))


def fontView(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Font settings'
    saver.savePref(uid, 'Action', 'font')
    bot.sendMessage(update.message.chat_id,
                    text=settings['font']['message'].format(saver.openPref(uid, 'font_size', 1)),
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('font', uid)))


def bottomTextView(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Top'
    saver.savePref(uid, 'Action', 'bottom')
    saver.savePref(uid, 'Bottom', '')
    bot.sendMessage(update.message.chat_id,
                    text=settings['bottom']['message'],
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('top', uid)))


def sendImageView(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Sending Image'
    saver.savePref(uid, 'Action', 'send_image')
    bot.sendMessage(update.message.chat_id,
                    text=settings['send_image']['message'],
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('send_image', uid)))


def adminView(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Admin panel'
    saver.savePref(uid, 'Action', 'admin')
    bot.sendMessage(update.message.chat_id,
                    text=settings['admin']['message'],
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('admin', uid)))


def sendMsgView(bot, update):
    uid = update.message.from_user.id
    if uid in saver.getAdmins():
        settings = actions.getBotSettings(uid)
        message_dict = update.to_dict()
        event_name = 'Sending message'
        saver.savePref(uid, 'Action', 'sendmsg')
        bot.sendMessage(update.message.chat_id,
                        text=settings['sendmsg']['message'],
                        reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('sendmsg', uid)))
    else:
        menuView(bot, update)


def previousImage(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Previous image'
    bot.sendChatAction(chat_id=uid, action=telegram.ChatAction.TYPING)
    if os.path.exists('images/in_' + str(uid) + '.jpg'):
        generator.make_meme(saver.openPref(uid, 'Top', ''),
                            saver.openPref(uid, 'Bottom', ''),
                            'images/in_' + str(uid) + '.jpg', uid, bot)
        menuView(bot, update)
    else:
        bot.sendMessage(update.message.chat_id,
                        text=settings['bottom']['message'],
                        reply_markup=actions.getKeyboard('top', uid))


def getLangsView(bot, update):
    uid = update.message.from_user.id
    menu = np.array([])
    settings = actions.getBotSettings(uid)
    for key, value in actions.locales.items():
        menu = np.append(menu, key)
    menu = np.reshape(menu, (-1, 1))
    saver.savePref(uid, 'Action', 'pick_language')
    bot.sendMessage(uid, text=settings['system_messages']['pick_lang'],
                    reply_markup=telegram.ReplyKeyboardMarkup(keyboard=menu))


def sendIt(bot, update):
    uid = update.message.from_user.id
    settings = actions.getBotSettings(uid)
    if uid in saver.getAdmins():
        for user in saver.getUsers():
            actions.sendMessage(bot, update, user)
    else:
        menuView(bot, update)


def performIt(bot, update, act):
    if act == 'menu':
        menuView(bot, update)
    elif act == 'top':
        topTextView(bot, update)
    elif act == 'admin':
        adminView(bot, update)
    elif act == 'sendmsg':
        sendMsgView(bot, update)
    elif act == 'bottom':
        bottomTextView(bot, update)
    elif act == 'feedback':
        feedbackView(bot, update)
    elif act == 'send_image':
        sendImageView(bot, update)
    elif act == 'previous_image':
        previousImage(bot, update)
    elif act == 'settings':
        settingsView(bot, update)
    elif act == 'caps':
        capsView(bot, update)
    elif act == 'reset':
        resetEveryone(bot, update)
    elif act == 'font':
        fontView(bot, update)
    elif act == 'caps_on':
        saver.savePref(update.message.chat_id, 'caps', True)
        settingsView(bot, update)
    elif act == 'caps_off':
        saver.savePref(update.message.chat_id, 'caps', False)
        settingsView(bot, update)
    elif act == 'lang':
        getLangsView(bot, update)


def menuView(bot, update, user_id = -1):
    uid = update.message.chat_id
    if user_id != -1:
        uid = user_id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Menu'
    print(telegram.ReplyKeyboardMarkup(actions.getKeyboard('menu', uid)))
    saver.savePref(uid, 'Action', 'menu')
    bot.sendMessage(uid,
                    text=settings['menu']['message'],
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('menu', uid)))


def feedbackView(bot, update):
    uid = update.message.chat_id
    settings = actions.getBotSettings(uid)
    message_dict = update.to_dict()
    event_name = 'Feedback'
    bot.sendMessage(update.message.chat_id,
                    text=settings['system_messages']['feedback'])
    menuView(bot, update)


def settingsView(bot, update):
    uid = update.message.chat_id
    settings = actions.getBotSettings(uid)
    saver.savePref(uid, 'Action', 'settings')
    message_dict = update.to_dict()
    event_name = 'Settings managing'
    bot.sendMessage(update.message.chat_id, text=settings['settings']['message'],
                    reply_markup=telegram.ReplyKeyboardMarkup(actions.getKeyboard('settings', uid)))


def cancel(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Cancel'
    menuView(bot, update)


def texting(bot, update):
    uid = update.message.chat_id
    act = saver.openPref(uid, 'Action', 'menu')
    message_dict = update.to_dict()
    event_name = 'Message'
    try:
        settings = actions.getBotSettings(uid)
        if act in settings:
            for option in settings[act]['keyboard']:
                if option['text'] == update.message.text:
                    performIt(bot, update, option['action'])
                    return None
        if act == 'top':
            saver.savePref(uid, 'Top', update.message.text)
            bottomTextView(bot, update)
        elif act == 'bottom':
            saver.savePref(uid, 'Bottom', update.message.text)
            sendImageView(bot, update)
        elif act == 'sendmsg':
            sendIt(bot, update)
            adminView(bot, update)
        elif act == 'pick_language':
            actions.setLocale(uid, update.message.text)
            settingsView(bot, update)
        elif act.endswith('font'):
            try:
                sz = float(update.message.text)
                if sz < 0:
                    sz = 0.01
                saver.savePref(uid, 'font_size', sz)
                bot.sendMessage(uid, text=settings['system_message']['jobs_finished'])
                settingsView(bot, update)

            except:
                bot.sendMessage(uid, text=settings['system_message']['number_parse_error'])
            settings(bot, update)
    except Exception as ex:
        print(ex)

def resetEveryone(bot, update):
    try:
        for user in saver.getUsers():
            menuView(bot, update, user_id=user)
    except:
        bot.sendMessage(chat_id=update.message.from_user.id, text='Bot were blocked by user?')

def image(bot, update):
    uid = update.message.from_user.id
    action = saver.openPref(uid, 'Action', 'menu')
    message_dict = update.to_dict()
    event_name = 'Photo'
    settings = actions.getBotSettings(uid)
    if action == 'send_image':
        if update.message.photo:
            try:
                bot.sendChatAction(chat_id=uid, action=telegram.ChatAction.TYPING)
                bot.sendMessage(uid, settings['system_messages']['hold_on'])
                bot.getFile(update.message.photo[-1].file_id).download('images/in_' + str(uid) + '.jpg')
                generator.make_meme(saver.openPref(uid, 'Top', ''),
                                    saver.openPref(uid, 'Bottom', ''),
                                    'images/in_' + str(uid) + '.jpg', uid, bot)
            except Exception as ex:
                bot.sendMessage(uid, 'Error occurred {}'.format(str(ex)))
            finally:
                menuView(bot, update)
    elif update.message.caption:
        lines = update.message.caption.split('/')
        saver.savePref(uid, 'Bottom', lines[0])
        if len(lines) > 1:
            saver.savePref(uid, 'Top', lines[1])
        bot.getFile(update.message.photo[-1].file_id).download('images/in_' + str(uid) + '.jpg')
        generator.make_meme(saver.openPref(uid, 'Top', ''),
                            saver.openPref(uid, 'Bottom', ''),
                            'images/in_' + str(uid) + '.jpg', uid, bot)


with open('key.config', 'r') as myfile:  # You must put key in key.config!!! IMPORTANT!!!!
    key = myfile.read().replace('\n', '')

if len(saver.getAdmins()) == 0:
    id = input('Enter admin ID: ')
    saver.savePref(id, 'is_admin', True)



from telegram.ext import MessageHandler, Filters


updater = Updater(key)
updater.dispatcher.add_handler(CommandHandler('start', menuView))
updater.dispatcher.add_handler(CommandHandler('create', topTextView))
updater.dispatcher.add_handler(CommandHandler('settings', settingsView))
updater.dispatcher.add_handler(CommandHandler('cancel', menuView))
updater.dispatcher.add_handler(
    MessageHandler(Filters.text | Filters.sticker | Filters.audio | Filters.document, texting))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, image))

updater.start_polling()
updater.idle()
