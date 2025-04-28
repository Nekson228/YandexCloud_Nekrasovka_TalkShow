from telebot import TeleBot
from telebot.types import Message

from src.bot.queue_manager import QueueManager


def setup_handlers(bot: TeleBot, queue_manager: QueueManager) -> None:
    @bot.message_handler(commands=['start'])
    def handle_start(message: Message):
        welcome = (
            f"Привет, {message.from_user.first_name}! "
            "Я создан для предоставления дайджестов по газетам.\n\n"
            "**Пример запроса:**\n"
            "*Новости спорта за январь 1936*"
        )
        bot.send_message(message.chat.id, welcome)

    @bot.message_handler(content_types=['text'])
    def handle_text(message: Message):
        chat_id = message.chat.id
        query = message.text

        bot.send_message(chat_id, f"Запрос принят: {query}")

        position = queue_manager.add_request(chat_id, query)
        if position > 0:
            bot.send_message(
                chat_id,
                f"Ваше место в очереди: {position}\n"
                f"Примерное время ожидания: {position * 0.25:.1f} мин."
            )
