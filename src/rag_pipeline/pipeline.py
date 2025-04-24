from pathlib import Path

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk._models.completions.model import GPTModel

from pandas import Series

from .data.loader import DataLoader
from .uploading.uploader import FileUploader
from .indexing.builder import IndexBuilder
from .assistant.manager import AssistantManager


def format_text(record: Series) -> str:
    return (
        f"{record['date']}\n"
        f"{record['source']}\n"
        f"{record.get('topic', '')}\n"
        f"{record.get('summary', '')}\n"
        f"{', '.join(record.get('entities', []))}\n"
        f"{record['content']}"
    )


class RAGPipeline:
    """
    A class to handle the RAG pipeline for Yandex Cloud ML SDK.
    """

    def __init__(self, sdk: YCloudML, model: GPTModel, data_path: Path) -> None:
        """
        Initialize the RAG pipeline with the given parameters.

        :param sdk: Yandex Cloud ML SDK instance.
        :param model: GPT model instance.
        :param data_path: Path to the directory containing JSON files for search index.
        """
        self.data_loader = DataLoader(data_path)
        self.file_uploader = FileUploader(sdk)
        self.index_builder = IndexBuilder(sdk)
        self.assistant_manager = AssistantManager(sdk, model)
        self.sdk = sdk

    def run(self, instruction: str, upload_files: bool = True) -> None:
        df = self.data_loader.load()
        texts = [format_text(row) for _, row in df.iterrows()]
        file_ids = self.file_uploader.upload(texts, upload_files)
        index = self.index_builder.build_index(file_ids)
        self.assistant_manager.index = index
        self.assistant_manager.setup(instruction)

    def query(self, question: str) -> str:
        return self.assistant_manager.ask(question)
