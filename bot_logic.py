#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, generator, telegram, botan
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

with open('botan.config', 'r') as myfile: #You must put key for your bot in botan.config!!! IMPORTANT!!!!
    botan_token=myfile.read().replace('\n', '')

class Chat:
    def __init__(self, id):
        self.id = id
        self.step = 0
        self.first = ''
        self.second = ''


    def manageSteps(self, bot, message):
        self.step = self.step + 1
        if (self.step == 1):
            self.firstStep(bot, message)
        elif (self.step == 2):
            self.secondStep(bot, message)
        elif (self.step == 3):
            self.thirdStep(bot, message)

    def firstStep(self, bot, message):
        if message.text == '[NONE TEXT]':
            self.first = ''
        else:
            self.first = message.text
        #print('First step:'+self.first)
        bot.sendMessage(self.id, text='Okay! Now, what do you want to see on bottom of image?', reply_markup=telegram.ReplyKeyboardMarkup([['[NONE TEXT]']]))

    def secondStep(self, bot, message):
        if message.text == '[NONE TEXT]':
            self.second = ''
        else:
            self.second = message.text
        bot.sendMessage(self.id, text='Nice! Send me a picture', reply_markup=telegram.ReplyKeyboardHide())

    def thirdStep(self, bot, message):
        if message.photo:
            bot.sendChatAction(chat_id=message.chat_id, action=telegram.ChatAction.TYPING)
            bot.sendMessage(message.chat_id, 'Hold on. I trying to download image.')
            bot.getFile(message.photo[-1].file_id).download('images/in_' + str(message.chat_id)+'.jpg')
            print('User '+str(self.id)+'. Uploaded picture with '+self.first + ' at top and '+ self.second+' at bottom')
            generator.make_meme(self.first, self.second, 'images/in_' + str(message.chat_id)+'.jpg', self.id, bot)
            chats.remove(self)

        else:
            self.step = self.step - 1
            bot.sendMessage(message.chat_id, 'Send me a picture, not this!')


chats = list()

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
    for chat in chats:
        if chat.id == update.message.chat_id:
            chats.remove(chat)
            break
    chat = Chat(update.message.chat_id)
    chats.append(chat)
    bot.sendMessage(update.message.chat_id, text='Let\'s start! Now what you what on top of image?', reply_markup=telegram.ReplyKeyboardMarkup([['[NONE TEXT]']]))



def texting(bot, update):
    uid = update.message.chat_id
    message_dict = update.to_dict()
    event_name = 'Message or photo'
    botan.track(botan_token, uid, message_dict, event_name)
    gotcha = False
    for chat in chats:
        if chat.id == update.message.chat_id:
            chat.manageSteps(bot, update.message)
            gotcha = True
    if gotcha == False:
        bot.sendMessage(update.message.chat_id, text='Write /create to begin!')

with open('key.config', 'r') as myfile: #You must put key in key.config!!! IMPORTANT!!!!
    key=myfile.read().replace('\n', '')

updater = Updater(key)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('create', create))
updater.dispatcher.add_handler(CommandHandler('feedback', feedback))
from telegram.ext import MessageHandler, Filters
updater.dispatcher.add_handler(MessageHandler([Filters.text], texting))
updater.dispatcher.add_handler(MessageHandler([Filters.photo], texting))


updater.start_polling()
updater.idle()