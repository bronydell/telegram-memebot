#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from tg import saver
from core import tools as actions, views as view
from threading import Thread


def generate_meme(sender):
    top_text = sender.get_preference('Top', '')
    bottom_text = sender.get_preference('Bottom', '')
    caps = sender.get_preference('Caps', False)
    font_size = sender.get_preference('font_size', False)
    view.generate_meme(sender, top_text=top_text, bottom_text=bottom_text, caps=caps, font_size=font_size)


def mail_everyone(sender):
    for user in saver.get_users():
        sender.user_id = user
        sender.chat_id = user
        actions.send_message(sender, sender.update.message.text)


def mail(sender):
    if sender.is_admin():
        thread = Thread(target=mail_everyone, args=sender)
        thread.start()
    else:
        view.menu(sender)


def perform_action(sender, act):
    if act == 'menu':
        view.menu(sender)
    elif act == 'top':
        view.top_text_menu(sender)
    elif act == 'admin':
        view.admin_menu(sender)
    elif act == 'sendmsg':
        view.send_msg_menu(sender)
    elif act == 'bottom':
        view.bottom_text_menu(sender)
    elif act == 'feedback':
        view.feedback(sender)
    elif act == 'send_image':
        view.send_image(sender)
    elif act == 'previous_image':
        generate_meme(sender)
    elif act == 'settings':
        view.user_settings(sender)
    elif act == 'caps':
        view.caps_settings(sender)
    elif act == 'font':
        view.font_settings(sender)
    elif act == 'caps_on':
        sender.save_preference('caps', True)
        view.user_settings(sender)
    elif act == 'caps_off':
        sender.save_preference('caps', False)
        view.user_settings(sender)
    elif act == 'lang':
        view.language_menu(sender)


def cancel_entry_point(sender):
    view.menu(sender)


def menu_entry_point(sender):
    view.menu(sender)


def settings_entry_point(sender):
    view.user_settings(sender)


def create_entry_point(sender):
    view.top_text_menu(sender)


def text_entry_point(sender):
    act = sender.get_preference('Action', 'menu')
    try:
        settings = sender.get_bot_settings()
        if act in settings:
            for option in settings[act]['keyboard']:
                if option['text'] == sender.update.message.text:
                    perform_action(sender, option['action'])
                    return None
        if act == 'top':
            sender.save_preference('Top', sender.update.message.text)
            view.bottom_text_menu(sender)
        elif act == 'bottom':
            sender.save_preference('Bottom', sender.update.message.text)
            view.send_image(sender)
        elif act == 'sendmsg':
            mail(sender)
            view.admin_menu(sender)
        elif act == 'pick_language':
            actions.set_locale(sender, sender.update.message.text)
            view.user_settings(sender)
        elif act.endswith('font'):
            try:
                sz = float(sender.update.message.text)
                if sz < 0:
                    sz = 0.01
                if sz > 5:
                    sz = 5
                sender.save_preference('font_size', sz)
                sender.send_message(text=settings['system_messages']['jobs_finished'])
            except ValueError:
                sender.send_message(text=settings['system_messages']['number_parse_error'])
            finally:
                view.user_settings(sender)
    except Exception as ex:
        print(ex)


def image_entry_point(sender):
    action = sender.get_preference('Action', 'menu')
    if action == 'send_image':
        try:
            if sender.download_image(path='images/in_{}.jpg'.format(sender.user_id)):
                generate_meme(sender)
        except Exception as ex:
            sender.send_message(text='Error occurred {}'.format(str(ex)))
            view.menu(sender)
    elif sender.update.message.caption:
        lines = sender.update.message.caption.split('/')
        sender.save_preference('Bottom', lines[0])
        if len(lines) > 1:
            sender.save_preference('Top', lines[1])
        else:
            sender.save_preference('Top', '')
        if sender.download_image(path='images/in_{}.jpg'.format(sender.user_id)):
            generate_meme(sender)
