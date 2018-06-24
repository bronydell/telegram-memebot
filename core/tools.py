import json
import time
from telegram.error import Unauthorized, RetryAfter

locales = {
    'English': 'bot.json',
    'Русский': 'bot_ru.json'
}


def set_locale(sender, message):
    if message in locales:
        sender.save_preference('locale', locales[message])


def send_message(sender, text=None):
    try:
        sender.sendMessage(text=text)
        time.sleep(0.1)
    except Unauthorized:
        pass
    except RetryAfter as ex:
        time.sleep(ex.retry_after)
        send_message(sender, text)
    except:
        pass


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def action(action_id, admin_only=False):
    def decorator(func):
        def decorate_action(sender, *args, **kwargs):
            if not admin_only or sender.is_admin():
                sender.save_preference('Action', action_id)
                func(sender, *args, **kwargs)

        return decorate_action

    return decorator
