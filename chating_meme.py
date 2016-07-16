import telegram, generator

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
            bot.sendMessage(message.chat_id, 'Hold on. I\'m trying to download the image.')
            bot.getFile(message.photo[-1].file_id).download('images/in_' + str(message.chat_id)+'.jpg')
            generator.make_meme(self.first, self.second, 'images/in_' + str(message.chat_id)+'.jpg', self.id, bot)

        else:
            self.step = self.step - 1
            bot.sendMessage(message.chat_id, 'Send me a picture, not this!')