import logging

from src.settings import FILES_CAP

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk._files.file import File

logger = logging.getLogger(__name__)


class FileUploader:
    """
    A class to upload files to Yandex Cloud ML.
    """

    def __init__(self, sdk: YCloudML, ttl_days: int = 1) -> None:
        self.sdk = sdk
        self.ttl_days = ttl_days

    def upload(self, texts: list[str], upload_files: bool) -> list[File]:
        if upload_files:
            return self._upload_files(texts)
        return self._retrieve_files()

    def _upload_files(self, texts: list[str]) -> list[File]:
        files: list[File] = []
        if FILES_CAP is not None:
            texts = texts[:FILES_CAP]
        logger.info(f"Uploading {len(texts)} files...")
        for i, text in enumerate(texts, 1):
            file_id = self.sdk.files.upload_bytes(text.encode(),
                                                  ttl_days=self.ttl_days, expiration_policy="static")
            files.append(file_id)
            if i % 100 == 0:
                logger.info(f"Uploaded {i}/{len(texts)}")
        logger.info(f"All files uploaded!")
        return files

    def _retrieve_files(self) -> list[File]:
        logger.info("Retrieving files...")
        files: list[File] = []
        files_loader = self.sdk.files.list()
        while True:
            if FILES_CAP is not None and len(files) >= FILES_CAP:
                break
            if len(files) % 100 == 0:
                logger.info(f"Retrieved {len(files)} files")
            try:
                files.append(next(files_loader))
            except StopIteration:
                break
        logger.info(f"Retrieved {len(files)} files!")
        return files
