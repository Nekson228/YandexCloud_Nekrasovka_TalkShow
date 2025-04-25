from collections.abc import Generator

import logging

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import (
    StaticIndexChunkingStrategy,
    HybridSearchIndexType,
    ReciprocalRankFusionIndexCombinationStrategy,
)
from yandex_cloud_ml_sdk._search_indexes.search_index import SearchIndex
from yandex_cloud_ml_sdk._files.file import File

logger = logging.getLogger(__name__)


class IndexBuilder:
    """
    Class for building a search index using Yandex Cloud ML SDK.
    """

    def __init__(self, sdk: YCloudML, chunk_size: int = 100) -> None:
        self.sdk = sdk
        self.chunk_size = chunk_size

    def chunk_list(self, items: list[File]) -> Generator[list[File]]:
        yield from (items[i:i + self.chunk_size]
                    for i in range(0, len(items), self.chunk_size))
        
        # if len(items) % self.chunk_size > 0:
        #     yield items[-(len(items) % self.chunk_size):]

    def build_index(self, file_ids: list[File]) -> SearchIndex:
        chunks = self.chunk_list(file_ids)
        index_type = HybridSearchIndexType(
            chunking_strategy=StaticIndexChunkingStrategy(
                max_chunk_size_tokens=1000,
                chunk_overlap_tokens=100
            ),
            combination_strategy=ReciprocalRankFusionIndexCombinationStrategy()
        )
        op = self.sdk.search_indexes.create_deferred(next(chunks), index_type=index_type)
        index = op.wait()
        for i, chunk in enumerate(chunks, 1):
            logger.info(f"Adding chunk {i} of length {len(chunk)}")
            op = index.add_files_deferred(chunk)
            op.wait()
        return index
