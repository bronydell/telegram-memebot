import saver
import telegram
import saver


def fontSettings(bot, update):
    uid = update.message.chat_id
    bot.sendMessage(uid, text='Send me scale of font(For example, 0.5 or 1). Current size is ' +
                                  str(saver.openPref(uid, 'font_size', 1)),
                    reply_markup=telegram.ReplyKeyboardHide())
    saver.savePref(uid, 'Action', 'settings_font')


