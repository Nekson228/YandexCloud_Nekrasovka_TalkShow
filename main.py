import logging

import telebot

from src.settings import BOT_TOKEN, FILTER_TEXTS
from src.services.ai import AIService
from src.services.speech import SpeechService
from src.bot.queue_manager import QueueManager
from src.bot.handlers import setup_handlers
from src.bot.utils import send_chunked_message


def main():
    ai_service = AIService(upload_files=True)
    speech_service = SpeechService()
    bot = telebot.TeleBot(BOT_TOKEN)

    def message_processor(chat_id: int, query: str):
        bot.send_message(chat_id, "⏳ Начинаю обработку запроса...")
        try:
            result = ai_service.process_query(query)

            if result in FILTER_TEXTS:
                raise ValueError("Content filter")

            clean_text = result.replace("#", "")
            send_chunked_message(bot, chat_id, clean_text)

            if audio := speech_service.synthesize(clean_text):
                bot.send_voice(chat_id, audio)
            else:
                bot.send_message(chat_id, "⚠️ Не удалось сгенерировать аудиоверсию")

        except Exception as e:
            error_msg = f"🚫 Ошибка обработки: {str(e)}"
            bot.send_message(chat_id, error_msg)

    queue_manager = QueueManager(process_callback=message_processor)

    setup_handlers(bot, queue_manager)

    logging.info("Starting bot polling...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
