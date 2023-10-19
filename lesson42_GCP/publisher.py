import logging
from concurrent import futures as futures_lib
from typing import Callable, Iterable, Optional

from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future

logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self, google_cloud_project: str, publish_timeout: int = 10):
        self._project_id = google_cloud_project
        self._pubsub = PublisherClient()
        self._publish_timeout = publish_timeout
        self._logger = logger

    @staticmethod
    def _publish_callback(future_: Future, timeout: int) -> Callable[[Future], None]:
        def callback(_) -> None:
            future_.result(timeout=timeout)

        return callback

    def _publish(self, message: bytes, topic: str, timeout: int = 10) -> Future:
        future = self._pubsub.publish(topic, message)
        future.add_done_callback(self._publish_callback(future, timeout=timeout))
        return future

    def publish_many(
        self,
        messages: Iterable,
        topic_id: str,
        timeout: Optional[int] = None,
    ) -> None:

        topic = self._pubsub.topic_path(self._project_id, topic_id)
        timeout = timeout or self._publish_timeout
        publish_futures = [
            self._publish(
                message.encode(encoding="UTF-8"),
                topic,
                timeout=timeout,
            )
            for message in messages
        ]
        futures_lib.wait(
            publish_futures, return_when=futures_lib.ALL_COMPLETED, timeout=timeout + 5
        )
        self._logger.debug(f"{len(publish_futures)} messages published OK to '{topic}'")

    def stop(self):
        self._pubsub.stop()
