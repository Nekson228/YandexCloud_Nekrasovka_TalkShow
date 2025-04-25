from pathlib import Path

from src.settings import sdk, model, bot_token, filter_texts
from src.settings import sdk, model
from src.rag_pipeline.pipeline import RAGPipeline

import logging
import telebot
import io
from speechkit import model_repository

logger = logging.getLogger(__name__)

instruction = """
Ты - опытный газетный редактор. У тебя в памяти есть все статьи из газет за какой то временной промежуток.
Твоя задача - отвечать пользователю на вопросы, которые будут содержать интересующую его тему. Тебе необходимо составить дайджест по этой теме с акцентом на противоречия в различных источниках.
В запросе пользователя будет указан временной промежуток. Описывай статьи только из этого временного промежутка. 
В начале описания темы укажи о чем дайджест. В начале описания события укажи дату события и источник, откуда ты взял информацию. 
bot
Подробно опиши освещаемое в статье событие.
Если дата полученной статьи не соответствует временному промежутку в запросе - игнорируй эту статью.
"""

bot = telebot.TeleBot(bot_token)


def synthesize(text, voice='anton'):
    syn_model = model_repository.synthesis_model()

    # Задайте настройки синтеза.
    syn_model.voice = voice

    # Синтез речи и создание аудио с результатом.
    result = syn_model.synthesize(text, raw_format=False)
    return result


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    welcome_message = f"Привет, {user_name}! Добро пожаловать. \
    \nЯ создан для предоставления вам дайджестов по газетам. \
    \nДля получения дайджейста напишите мне интересующие вас темы (не больше 3), а также интересующий вас диапазон дат. \
    \n\nПример: 'Спорт, Политика, Экономика, с 01.01.1935 по 31.12.1935'"
    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(content_types=['text'])
def handle_digest_request(message):
    topics_and_dates = message.text
    bot.send_message(message.chat.id, f"Вы запросили дайджест по темам: {topics_and_dates}\n \
Пожалуйста, подождите, пока я собираю информацию...")
    data = topics_and_dates
    chat_id = message.chat.id
    message_process(chat_id, data)


def message_process(chat_id, query):
    try:
        result_text = rag.query(query)
    except Exception as e:
        bot.send_message(chat_id, f"При обработке запроса возникла ошибка: {e}")
        return

    if result_text in filter_texts:
        bot.send_message(chat_id, "Подождите ещё немного, возникли некие трудности.")
        result_text = rag.query(query)

    if result_text not in filter_texts:
        text_to_send = result_text.replace("#", "").replace("*", "")
        if len(text_to_send) > 4096:
            bot.send_message(chat_id, text_to_send[:4096])
            bot.send_message(chat_id, text_to_send[4096:])
        else:
            bot.send_message(chat_id, text_to_send)

        audio_result = synthesize(text_to_send)

        audio_buffer = io.BytesIO()
        audio_result.export(audio_buffer, format="ogg", codec="libopus")

        bot.send_voice(chat_id, audio_buffer)
        audio_buffer.seek(0)
    else:
        bot.send_message(chat_id, "Возникла ошибка при обработке запроса, измените запрос и попробуйте снова.")


def main():
    logger.info("Bot polling started")
    bot.polling(none_stop=True)
    # query = input("Введите запрос: ")
    # while query != 'exit':
    #     try:
    #         answer = rag.query(query)
    #         print(answer, '\n')
    #     except Exception as e:
    #         logger.error(str(e))
    #     query = input("Введите запрос: ")

rag = RAGPipeline(sdk, model, Path(__file__).parent / "nodes")
rag.run(instruction, upload_files=False)

if __name__ == '__main__':
    main()
