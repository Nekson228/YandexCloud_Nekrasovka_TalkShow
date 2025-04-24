import os
from yandex_cloud_ml_sdk import YCloudML

from dotenv import load_dotenv

import logging

load_dotenv()

api_key = os.getenv("API_KEY")
folder_id = os.getenv("FOLDER_ID")

sdk = YCloudML(folder_id=folder_id, auth=api_key)
model = sdk.models.completions("yandexgpt", model_version="rc")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
