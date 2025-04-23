from dotenv import load_dotenv
import telebot
import os
import time

load_dotenv()
token = os.getenv("bot_token")
if token is None:
    raise ValueError("Environment variable 'TOKEN' is not set.")

bot = telebot.TeleBot(token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    welcome_message = f"Привет, {user_name}! Добро пожаловать. \
    \nЯ создан для предоставления вам дайджестов по газетам. \
    \nДля получения дайджейста напишите мне интересующие вас темы (не больше 3), а также интересующий вас диапазон дат. \
    \n\nПример: 'Спорт, Политика, Экономика, с 01.01.2023 по 31.12.2023'"
    bot.send_message(message.chat.id, welcome_message)



@bot.message_handler(content_types=['text'])
def handle_digest_request(message):
    topics_and_dates = message.text
    bot.send_message(message.chat.id, f"Вы запросили дайджест по темам: {topics_and_dates}\n \
Пожалуйста, подождите, пока я собираю информацию...")
    
# Функция для отправки текста пользователю
def send_message_to_user(chat_id, text):
    """
    Отправляет текстовое сообщение пользователю.
    
    Args:
        chat_id: ID чата пользователя
        text: Текст сообщения для отправки
    
    Returns:
        Объект отправленного сообщения
    """
    return bot.send_message(chat_id, text)

# Функция для отправки аудио пользователю
def send_audio_to_user(chat_id, audio_file, caption=None):
    """
    Отправляет аудиозапись пользователю.
    
    Args:
        chat_id: ID чата пользователя
        audio_file: Путь к аудиофайлу или file_id или файловый объект
        caption: Подпись к аудио (опционально)
    
    Returns:
        Объект отправленного сообщения
    """
    return bot.send_audio(chat_id, audio_file, caption=caption)

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)