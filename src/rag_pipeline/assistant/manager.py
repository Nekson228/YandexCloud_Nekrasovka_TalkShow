from typing import Optional

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk._assistants.assistant import Assistant, Thread
from yandex_cloud_ml_sdk._search_indexes.search_index import SearchIndex
from yandex_cloud_ml_sdk._models.completions.model import GPTModel

from src.utils.date_llm_parser import get_date_range_from_query


class AssistantManager:
    """
    A class to manage the assistant for Yandex Cloud ML SDK.
    """

    def __init__(self, sdk: YCloudML, model: GPTModel, index: Optional[SearchIndex] = None) -> None:
        self.sdk = sdk
        self.model = model
        self.index = index

        self.assistant: Optional[Assistant] = None
        self.thread: Optional[Thread] = None

    def setup(self, instruction: str) -> None:
        if self.index is None:
            raise ValueError("Index is not set.")

        search_tool = self.sdk.tools.search_index(self.index)
        self.assistant = self.sdk.assistants.create(
            self.model,
            ttl_days=1,
            expiration_policy="since_last_active",
            tools=[search_tool]
        )
        self.assistant.update(instruction=instruction)
        self.thread = self.sdk.threads.create(ttl_days=1, expiration_policy="static")

    def ask(self, query: str) -> str:
        if self.thread is None or self.assistant is None:
            raise RuntimeError("Assistant not initialized")

        self.thread.write(self.preprocess_query(query))
        run = self.assistant.run(self.thread)
        result = run.wait()
        return result.text

    def preprocess_query(self, query: str) -> str:
        return get_date_range_from_query(query).format_query()
