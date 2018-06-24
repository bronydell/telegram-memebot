import os
from core import generator
from telegram import ChatAction
from core.tools import locales, build_menu, action


@action('top')
def top_text_menu(sender):
    settings = sender.get_bot_settings()
    sender.save_preference('Top', '')
    sender.send_message(text=settings['top']['message'],
                        reply_markup=sender.get_keyboard('top'))


@action('bottom')
def bottom_text_menu(sender):
    settings = sender.get_bot_settings()
    sender.save_preference('Bottom', '')
    sender.send_message(text=settings['bottom']['message'],
                        reply_markup=sender.get_keyboard('top'))


@action('caps')
def caps_settings(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['caps']['message'],
                       reply_markup=sender.get_keyboard('caps'))


@action('font')
def font_settings(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['font']['message'].format(sender.get_preference('font_size', 1)),
                        reply_markup=sender.get_keyboard('font'))


@action('send_image')
def send_image(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['send_image']['message'],
                        reply_markup=sender.get_keyboard('send_image'))


@action('admin', admin_only=True)
def admin_menu(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['admin']['message'],
                        reply_markup=sender.get_keyboard('admin'))


@action('sendmsg', admin_only=True)
def send_msg_menu(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['sendmsg']['message'],
                        reply_markup=sender.get_keyboard('sendmsg'))


def generate_meme(sender, top_text, bottom_text, caps, font_size):
    settings = sender.get_bot_settings()
    if os.path.exists('images/in_' + str(sender.user_id) + '.jpg'):
        sender.send_message(text=settings['system_messages']['editing'])
        sender.send_chat_action(action=ChatAction.UPLOAD_PHOTO)
        image_path = generator.make_meme(top_text, bottom_text, sender.user_id, caps=caps, font_scale=font_size)
        sender.send_message(text=settings['system_messages']['uploading'])
        sender.send_photo(photo=open(image_path, 'rb'))
        menu(sender)
    else:
        sender.send_message(text=settings['bottom']['message'],
                            reply_markup=sender.get_keyboard('top'))


@action('pick_language')
def language_menu(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['system_messages']['pick_lang'],
                        reply_markup=build_menu(list(locales.keys()), n_cols=1))


@action('menu')
def menu(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['menu']['message'],
                        reply_markup=sender.get_keyboard('menu'))


def feedback(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['system_messages']['feedback'])
    menu(sender)


@action('settings')
def user_settings(sender):
    settings = sender.get_bot_settings()
    sender.send_message(text=settings['settings']['message'],
                        reply_markup=sender.get_keyboard('settings'))
