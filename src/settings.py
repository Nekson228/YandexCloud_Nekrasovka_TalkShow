import os
import logging
from pathlib import Path

from dotenv import load_dotenv

from yandex_cloud_ml_sdk import YCloudML
from speechkit import configure_credentials, creds

FILTER_TEXTS = [
    "В интернете есть много сайтов с информацией на эту тему. [Посмотрите, что нашлось в поиске](https://ya.ru)"
    "В интернете есть много сайтов с информацией на эту тему. [Посмотрите, что нашлось в поиске](https://ya.ru)."
]

AGENT_INSTRUCTION = """Ты - опытный газетный редактор. У тебя в памяти есть все статьи из газет за какой то временной промежуток.
Твоя задача - отвечать пользователю на вопросы, которые будут содержать интересующую его тему. Тебе необходимо составить дайджест по этой теме с акцентом на противоречия в различных источниках.
В запросе пользователя будет указан временной промежуток. Описывай статьи только из этого временного промежутка. 
В начале описания темы укажи о чем дайджест. В начале описания события укажи дату события и источник, откуда ты взял информацию. 
bot
Подробно опиши освещаемое в статье событие.
Если дата полученной статьи не соответствует временному промежутку в запросе - игнорируй эту статью.
"""

NODES_PATH = Path(__file__).parent.parent / "nodes"

FILES_CAP: int | None = 500

load_dotenv()

API_KEY = os.getenv("API_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

sdk = YCloudML(folder_id=FOLDER_ID, auth=API_KEY)
model = sdk.models.completions("llama", model_version="rc")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key=API_KEY
    )
)
