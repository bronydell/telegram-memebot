#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, chating_meme, telegram, botan
from telegram.ext import Updater, CommandHandler
import chating_settings

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

with open('botan.config', 'r') as myfile: #You must put key for your bot in botan.config!!! IMPORTANT!!!!
    botan_token=myfile.read().replace('\n', '')


meme_chats = list()
settings_chats = list()

def start(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'New User'
    botan.track(botan_token, uid, message_dict, event_name)
    bot.sendMessage(update.message.chat_id,
                    text='I can create any meme what you want! Go ahead and use /create command')

def feedback(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Feedback'
    botan.track(botan_token, uid, message_dict, event_name)
    bot.sendMessage(update.message.chat_id,
                    text='Feel free to share your feedback here: https://storebot.me/bot/creatememe_bot'
                         ' or you can write me directly: @bronydell')

def create(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Creating a meme'
    botan.track(botan_token, uid, message_dict, event_name)
    anti_burger(update)
    chat = chating_meme.Chat(update.message.chat_id)
    meme_chats.append(chat)
    bot.sendMessage(update.message.chat_id, text='Let\'s start! Now what you what on top of image?',
                    reply_markup=telegram.ReplyKeyboardMarkup([['[NONE TEXT]']]))

def anti_burger(update):

    for chat in settings_chats:
        if chat.id == update.message.chat_id:
            settings_chats.remove(chat)
            break

    for chat in meme_chats:
        if chat.id == update.message.chat_id:
            meme_chats.remove(chat)
            break

def settings(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Settings managing'
    botan.track(botan_token, uid, message_dict, event_name)
    anti_burger(update)
    chat = chating_settings.Chat(update.message.chat_id)
    settings_chats.append(chat)
    bot.sendMessage(update.message.chat_id, text='What do you want to change in your settings?',
                    reply_markup=telegram.ReplyKeyboardMarkup([['1. Font scale'],
                                                               ['2. Caps settings']]))

def cancel(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Cancel'
    botan.track(botan_token, uid, message_dict, event_name)
    anti_burger(update)
    bot.sendMessage(update.message.chat_id, text='Done', reply_markup=telegram.ReplyKeyboardHide())


def texting(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Message or photo'
    botan.track(botan_token, uid, message_dict, event_name)
    gotcha = False
    for chat in meme_chats:
        if chat.id == update.message.chat_id:
            chat.manageSteps(bot, update.message)
            if chat.step == 3:
                meme_chats.remove(chat)
            gotcha = True

    for chat in settings_chats:
        if chat.id == update.message.chat_id:
            chat.manageSteps(bot, update.message)
            if chat.step == 2:
                settings_chats.remove(chat)
            gotcha = True
    if gotcha == False:
        bot.sendMessage(update.message.chat_id, text='Write /create to begin or /settings to manage your account')

with open('key.config', 'r') as myfile: #You must put key in key.config!!! IMPORTANT!!!!
    key = myfile.read().replace('\n', '')

updater = Updater(key)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('create', create))
updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
updater.dispatcher.add_handler(CommandHandler('settings', settings))
updater.dispatcher.add_handler(CommandHandler('feedback', feedback))

from telegram.ext import MessageHandler, Filters
updater.dispatcher.add_handler(MessageHandler([Filters.text], texting))
updater.dispatcher.add_handler(MessageHandler([Filters.photo], texting))

updater.start_polling()
updater.idle()