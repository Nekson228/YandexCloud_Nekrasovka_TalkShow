import threading
from queue import Queue
import logging
from typing import Callable, NamedTuple

logger = logging.getLogger(__name__)


class RequestData(NamedTuple):
    chat_id: int
    query: str


class QueueManager:
    """
    Class to manage request queue
    """
    def __init__(self, process_callback: Callable):
        self.queue: Queue[RequestData] = Queue()
        self.process_thread = threading.Thread(
            target=self._process_requests,
            daemon=True
        )
        self.process_callback = process_callback
        self.process_thread.start()

    def add_request(self, chat_id: int, query: str) -> int:
        position = self.queue.qsize() + 1
        self.queue.put(RequestData(chat_id, query))
        return position

    def _process_requests(self):
        while True:
            request = self.queue.get()
            try:
                self.process_callback(request.chat_id, request.query)
            except Exception as e:
                logger.error(f"Request processing error: {e}")
            finally:
                self.queue.task_done()
