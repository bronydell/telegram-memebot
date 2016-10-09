#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, chating_meme, telegram, botan
from telegram.ext import Updater, CommandHandler
import chating_settings
import saver, generator
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

with open('botan.config', 'r') as myfile: #You must put key for your bot in botan.config!!! IMPORTANT!!!!
    botan_token=myfile.read().replace('\n', '')


def menu(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Menu'
    botan.track(botan_token, uid, message_dict, event_name)
    saver.savePref(uid, 'Action', 'menu')
    bot.sendMessage(update.message.chat_id,
                    text='Press "Create Meme", to create meme',
                    reply_markup = telegram.ReplyKeyboardMarkup([['Create Meme'],
                                                                 ['Settings'],
                                                                 ['Feedback']]))

def feedback(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Feedback'
    botan.track(botan_token, uid, message_dict, event_name)
    bot.sendMessage(update.message.chat_id,
                    text='Feel free to share your feedback here: https://storebot.me/bot/creatememe_bot'
                         ' or you can write me directly: @bronydell')
    menu(bot, update)

def create(bot, update):
    uid = update.message.chat_id
    saver.savePref(uid, 'Action', 'create_top')
    message_dict = update.to_dict()
    event_name = 'Creating a meme'
    botan.track(botan_token, uid, message_dict, event_name)
    bot.sendMessage(update.message.chat_id, text='Let\'s start! Now what you what at top of a image?',
                    reply_markup=telegram.ReplyKeyboardMarkup([['[NONE TEXT]']]))


def settings(bot, update):
    uid = update.message.chat_id
    saver.savePref(uid, 'Action', 'settings')
    message_dict = update.to_dict()
    event_name = 'Settings managing'
    botan.track(botan_token, uid, message_dict, event_name)
    bot.sendMessage(update.message.chat_id, text='What do you want to change in your settings?',
                    reply_markup=telegram.ReplyKeyboardMarkup([['Font scale'],
                                                               ['Caps settings'],
                                                               ['Menu']]))

def cancel(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Cancel'
    botan.track(botan_token, uid, message_dict, event_name)
    menu(bot, update)


def texting(bot, update):
    uid = update.message.chat_id
    action = saver.openPref(uid, 'Action', 'menu')
    message_dict = update.to_dict()
    event_name = 'Message'
    botan.track(botan_token, uid, message_dict, event_name)
    if action == 'menu':
        if update.message.text == 'Create Meme':
            create(bot, update)
        elif update.message.text == 'Settings':
            settings(bot, update)
        elif update.message.text == 'Feedback':
            feedback(bot, update)
    elif action == 'settings':
        if update.message.text == 'Font scale':
            chating_settings.fontSettings(bot, update)
        elif update.message.text == 'Caps settings':
            chating_settings.capsSettings(bot, update)
        elif update.message.text == 'Menu':
            menu(bot, update)
    elif action.startswith('settings_'):
        if action.endswith('caps'):
            if (update.message.text.startswith('Y')):
                saver.savePref(uid, 'caps', True)
                bot.sendMessage(uid, text="GOT IT", reply_markup=telegram.ReplyKeyboardHide())
            elif (update.message.text.startswith('N')):
                saver.savePref(uid, 'caps', False)
                bot.sendMessage(uid, text="Got it", reply_markup=telegram.ReplyKeyboardHide())
            else:
                bot.sendMessage(uid, text="I can't find this option")
        elif action.endswith('font'):
            try:
                sz = float(update.message.text)
                if (sz < 0):
                    sz = 0.01
                saver.savePref(uid, 'font_size', sz)
                bot.sendMessage(uid, text="Updated!")
            except:
                bot.sendMessage(uid, text="Parse error. Is this text a number?")
        settings(bot, update)
    elif action.startswith('create_'):
        if action.endswith('top'):
            chating_meme.saveTop(bot, update.message)
        elif action.endswith('bottom'):
            chating_meme.saveBottom(bot, update.message)


def image(bot, update):
    uid = update.message.chat_id
    action = saver.openPref(uid, 'Action', 'menu')
    message_dict = update.to_dict()
    event_name = 'Photo'
    botan.track(botan_token, uid, message_dict, event_name)
    if action.startswith('create_'):
        if action.endswith('image'):
            if update.message.photo:
                try:
                    bot.sendChatAction(chat_id=uid, action=telegram.ChatAction.TYPING)
                    bot.sendMessage(uid, 'Hold on. I\'m trying to download the image.')
                    bot.getFile(update.message.photo[-1].file_id).download('images/in_' + str(uid) + '.jpg')
                    generator.make_meme(saver.openPref(uid, 'Top', ''),
                                        saver.openPref(uid, 'Bottom', ''),
                                        'images/in_' + str(uid) + '.jpg', uid, bot)
                except Exception:
                    bot.sendMessage(uid, 'Error. Error. Error.')
                finally:
                    menu(bot, update)

with open('key.config', 'r') as myfile: #You must put key in key.config!!! IMPORTANT!!!!
    key = myfile.read().replace('\n', '')

updater = Updater(key)
updater.dispatcher.add_handler(CommandHandler('start', menu))
updater.dispatcher.add_handler(CommandHandler('create', create))
updater.dispatcher.add_handler(CommandHandler('settings', settings))
updater.dispatcher.add_handler(CommandHandler('cancel', menu))

from telegram.ext import MessageHandler, Filters
updater.dispatcher.add_handler(MessageHandler([Filters.text], texting))
updater.dispatcher.add_handler(MessageHandler([Filters.photo], image))

updater.start_polling()
updater.idle()