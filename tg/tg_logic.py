from core import logic
from tg.sender import Sender


def telegram_text_entry(bot, update):
    sender = Sender(bot, update)
    logic.text_entry_point(sender)


def telegram_image_entry(bot, update):
    sender = Sender(bot, update)
    logic.image_entry_point(sender)


def telegram_menu_entry(bot, update):
    sender = Sender(bot, update)
    logic.menu_entry_point(sender)


def telegram_cancel_entry(bot, update):
    sender = Sender(bot, update)
    logic.cancel_entry_point(sender)


def telegram_settings_entry(bot, update):
    sender = Sender(bot, update)
    logic.settings_entry_point(sender)


def telegram_create_entry(bot, update):
    sender = Sender(bot, update)
    logic.create_entry_point(sender)
