from src.rag_pipeline.pipeline import RAGPipeline
from src.settings import sdk, model, AGENT_INSTRUCTION, NODES_PATH


class AIService:
    """
    Service wrapper for RAG
    """
    def __init__(self, upload_files: bool = False):
        self.rag = RAGPipeline(sdk, model, NODES_PATH)
        self.rag.run(AGENT_INSTRUCTION, upload_files=upload_files)

    def process_query(self, query: str) -> str:
        return self.rag.query(query)
