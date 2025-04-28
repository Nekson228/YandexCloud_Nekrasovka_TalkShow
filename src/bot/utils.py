import telebot


def send_chunked_message(bot: telebot.TeleBot, chat_id: int, text: str, max_length: int = 4096):
    for i in range(0, len(text), max_length):
        chunk = text[i:i + max_length]
        bot.send_message(chat_id, chunk)
