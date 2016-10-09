import telegram, generator, saver


def saveTop(bot, message):
    if message.text == '[NONE TEXT]':
        saver.savePref(message.chat_id, 'Top', '')
    else:
        saver.savePref(message.chat_id, 'Top', message.text)
    bot.sendMessage(message.chat_id, text='Okay! Now, what do you want to see at bottom of the image?',
                    reply_markup=telegram.ReplyKeyboardMarkup([['[NONE TEXT]']]))
    saver.savePref(message.chat_id, 'Action', 'create_bottom')

def saveBottom(bot, message):
    if message.text == '[NONE TEXT]':
        saver.savePref(message.chat_id, 'Bottom', '')
    else:
        saver.savePref(message.chat_id, 'Bottom', message.text)
    bot.sendMessage(message.chat_id, text='Good. Upload your image',
                    reply_markup=telegram.ReplyKeyboardMarkup([['[NONE TEXT]']]))
    saver.savePref(message.chat_id, 'Action', 'create_image')
