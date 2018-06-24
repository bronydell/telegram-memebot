from tg import saver, tg_logic
from telegram.ext import MessageHandler, Filters, CommandHandler, Updater


def run():
    with open('key.config', 'r') as file:
        key = file.read().replace('\n', '')

    if len(saver.get_admins()) == 0:
        admin_id = input('Enter admin ID: ')
        saver.save_pref(admin_id, 'is_admin', True)

    updater = Updater(key)
    updater.dispatcher.add_handler(CommandHandler('start', tg_logic.telegram_menu_entry))
    updater.dispatcher.add_handler(CommandHandler('create', tg_logic.telegram_create_entry))
    updater.dispatcher.add_handler(CommandHandler('settings', tg_logic.telegram_settings_entry))
    updater.dispatcher.add_handler(CommandHandler('cancel', tg_logic.telegram_cancel_entry))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text | Filters.sticker | Filters.audio | Filters.document, tg_logic.telegram_text_entry))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, tg_logic.telegram_image_entry))

    updater.start_polling()
    updater.idle()