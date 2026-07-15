import telebot

# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН (после того как сделаешь /revoke в @BotFather)
TOKEN = '8953017967:AAEG2e7BxoWv2UoKgh5Ay16_7eK1AYTNW_E'
bot = telebot.TeleBot(TOKEN)

# Список Telegram ID админов бота
BOT_ADMINS = [8576627424]

# Глобальные переменные
bound_chat_id = None
phone_number = '+7 999 123-45-67'

def is_bot_admin(user_id):
    return user_id in BOT_ADMINS

@bot.message_handler(commands=['bind'])
def bind_chat(message):
    global bound_chat_id
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_bot_admin(user_id):
        bot.reply_to(message, 'У вас нет прав на эту команду.')
        return

    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, 'Эта команда работает только в группах.')
        return

    bound_chat_id = chat_id
    bot.reply_to(message, f'✅ Бот привязан к этой группе (ID: {chat_id}).\nТеперь он отвечает на "слет" и "номер" только здесь.')

@bot.message_handler(commands=['setphone'])
def set_phone(message):
    global phone_number
    user_id = message.from_user.id

    if not is_bot_admin(user_id):
        bot.reply_to(message, 'У вас нет прав на эту команду.')
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, 'Напишите номер после команды, например:\n/setphone +7 999 888-77-66')
        return

    new_number = parts[1].strip()
    if not new_number:
        bot.reply_to(message, 'Номер не может быть пустым.')
        return

    phone_number = new_number
    bot.reply_to(message, f'✅ Номер обновлён: {phone_number}')

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    # Игнорируем сообщения не из привязанной группы
    if bound_chat_id is None or message.chat.id != bound_chat_id:
        return

    text = message.text or ''
    if 'слет' in text.lower() or 'номер' in text.lower():
        bot.reply_to(message, phone_number)

if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)
