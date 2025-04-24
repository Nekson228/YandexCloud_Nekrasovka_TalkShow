from pathlib import Path

from src.settings import sdk, model
from src.rag_pipeline.pipeline import RAGPipeline

import logging

logger = logging.getLogger(__name__)

instruction = """
Ты - опытный газетный редактор. У тебя в памяти есть все статьи из газет за какой то временной промежуток.
Твоя задача - отвечать пользователю на вопросы, которые будут содержать интересующую его тему. Тебе необходимо составить дайджест по этой теме с акцентом на противоречия в различных источниках.
В запросе пользователя будет указан временной промежуток. Описывай статьи только из этого временного промежутка. 
В начале описания темы укажи о чем дайджест. В начале описания события укажи дату события и источник, откуда ты взял информацию. 
Подробно опиши освещаемое в статье событие. 
"""

def main():
    rag = RAGPipeline(sdk, model, Path(__file__).parent / "nodes")
    rag.run(instruction, upload_files=False)
    query = input("Введите запрос: ")
    while query != 'exit':
        try:
            answer = rag.query(query)
            print(answer, '\n')
        except Exception as e:
            logger.error(str(e))
        query = input("Введите запрос: ")


if __name__ == '__main__':
    main()