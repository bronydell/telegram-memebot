import telegram, saver

class Chat:
    def __init__(self, id):
        self.id = id
        self.step = 0
        self.setting = ''

    def manageSteps(self, bot, message):
        self.step = self.step + 1
        if (self.step == 1):
            self.firstStep(bot, message)
        elif (self.step == 2):
            self.secondStep(bot, message)

    def firstStep(self, bot, message):
        '''if(message.text.startswith('1')):
            self.setting = 'lang'
            bot.sendMessage(self.id, text = 'What is your language? Current is '
                                            + str(saver.openPref(self.id, 'lang', 'english')),
                            reply_markup=telegram.ReplyKeyboardMarkup([['English'],
                                                                    ['Russian']]))
        '''
        if (message.text.startswith('1')):
            self.setting = 'font_size'
            bot.sendMessage(self.id, text='Send me scale of font(For example, 0.5 or 1). Current is ' +
                                          str(saver.openPref(self.id, 'font_size', 1)),
                            reply_markup=telegram.ReplyKeyboardHide())
        elif (message.text.startswith('2')):
            self.setting = 'caps'
            bot.sendMessage(self.id, text='Turn this feature on?', reply_markup=telegram.ReplyKeyboardMarkup([['Yes'],
                                                                                                 ['No']]))
        else:
            bot.sendMessage(self.id, text="I don't know what are you talking about.")
            self.step-=1

    def secondStep(self, bot, message):
        '''#Language settings
        if(self.setting=='lang'):
            if(message.text.startswith('Eng')):
                saver.savePref(self.id, 'lang', 'english')
                bot.sendMessage(self.id, text="Done")
            elif(message.text.startswith('Rus')):
                saver.savePref(self.id, 'lang', 'russian')
                bot.sendMessage(self.id, text="Готово")
            else:
                bot.sendMessage(self.id, text="I can't find this language")
        '''
        #Capslock settings
        if(self.setting=='caps'):
            if(message.text.startswith('Y')):
                saver.savePref(self.id, 'caps', True)
                bot.sendMessage(self.id, text="GOT IT", reply_markup=telegram.ReplyKeyboardHide())
            elif(message.text.startswith('N')):
                saver.savePref(self.id, 'caps', False)
                bot.sendMessage(self.id, text="Got it", reply_markup=telegram.ReplyKeyboardHide())
            else:
                bot.sendMessage(self.id, text="I can't find this option")

        #Font size settings
        if(self.setting=='font_size'):
            try:
                sz = float(message.text)
                if(sz<0):
                    sz=0.01
                saver.savePref(self.id, 'font_size', sz)
                bot.sendMessage(self.id, text="Updated!")
            except:
                bot.sendMessage(self.id, text="Parse error. Is this text a number?")






