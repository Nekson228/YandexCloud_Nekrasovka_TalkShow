import os
from yandex_cloud_ml_sdk import YCloudML

from dotenv import load_dotenv

import logging


from speechkit import configure_credentials, creds

filter_texts = [
    "В интернете есть много сайтов с информацией на эту тему. [Посмотрите, что нашлось в поиске](https://ya.ru)"
    "В интернете есть много сайтов с информацией на эту тему. [Посмотрите, что нашлось в поиске](https://ya.ru)."
]
load_dotenv()

api_key = os.getenv("API_KEY")
folder_id = os.getenv("FOLDER_ID")
bot_token = os.getenv("BOT_TOKEN")

sdk = YCloudML(folder_id=folder_id, auth=api_key)
model = sdk.models.completions("yandexgpt", model_version="rc")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key=api_key
    )
)
