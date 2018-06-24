import telegram
import os
import json
from tg import saver
from core.tools import build_menu


class Sender:
    def __init__(self, bot, update):
        self.bot = bot
        self.update = update
        self.user_id = update.effective_user.id
        self.chat_id = update.effective_message.chat_id

    def send_chat_action(self, action):
        self.bot.send_chat_action(self.chat_id, action=action)

    def send_photo(self, photo):
        self.bot.send_photo(self.chat_id, photo=photo)

    def download_image(self, path):
        if self.update.message.photo:
            self.bot.getFile(self.update.message.photo[-1].file_id).download(path)
            return True
        else:
            return False

    def send_message(self, text, reply_markup=None):
        if reply_markup:
            self.bot.send_message(self.chat_id,
                                  text=text,
                                  reply_markup=telegram.ReplyKeyboardMarkup(reply_markup))
        else:
            self.bot.send_message(self.chat_id, text=text)

    def get_bot_settings(self):
        with open(self.get_preference('locale', 'bot.json'), encoding='UTF-8') as data_file:
            data = json.load(data_file)
        return data

    def save_preference(self, key, value):
        return saver.save_pref(self.user_id, key, value)

    def get_preference(self, key, default_value):
        return saver.open_pref(self.user_id, key, default_value)

    def is_admin(self):
        return self.get_preference('is_admin', False)

    def get_keyboard(self, tag):
        settings = self.get_bot_settings()
        menu = []
        for option in settings[tag]['keyboard']:
            if 'admin_only' in option:
                if self.get_preference('is_admin', False) or not option['admin_only']:
                    menu.append(option['text'])
            elif 'had_image' in option:
                if os.path.exists('images/in_' + str(self.user_id) + '.jpg'):
                    menu.append(option['text'])
            else:
                menu.append(option['text'])
        return build_menu(menu, 1)
