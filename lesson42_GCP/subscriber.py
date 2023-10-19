import json
import logging
import signal
from concurrent.futures import ThreadPoolExecutor

import google.cloud.pubsub_v1.subscriber.message as pubsub_message
from google.cloud.pubsub_v1 import SubscriberClient
from google.cloud.pubsub_v1.subscriber.scheduler import ThreadScheduler

from lesson42_GCP.utils import get_current_datetime_str
from lesson42_GCP.processor import Processor


logger = logging.getLogger(__name__)


class SubscriberStartError(Exception):
    """
    Raises when the main process is not started
    """


class SubscriberStopError(Exception):
    """
    Raises when the main process is stopped by receiving the OS signal
    """


def _handler_stop_signals(signum, frame):
    raise SubscriberStopError(
        "SIGTERM" if signum == 15 else "SIGHUP", get_current_datetime_str()
    )


def register_signals():
    signal.signal(signal.SIGHUP, _handler_stop_signals)
    signal.signal(signal.SIGTERM, _handler_stop_signals)


register_signals()


class Subscriber:

    DATA_HANDLER_EXPECTED_METHODS = ("start_processing", "stop")

    def __init__(
        self,
        google_cloud_project: str,
        subscription_id: str,
        processor: Processor,
        redeliver_message: bool = False,
        max_threads_workers: int = 20,
    ):
        self._logger = logger
        self._subscriber = SubscriberClient()
        self.subscription = self._subscriber.subscription_path(
            project=google_cloud_project,
            subscription=subscription_id
        )
        self.redeliver_messages = redeliver_message
        self._processor = processor
        self._max_threads_workers = max_threads_workers

    @property
    def callback(self):
        return (
            self._process_message_with_redelivering_on_error
            if self.redeliver_messages
            else self._process_message_with_no_redelivering
        )

    def run(self):
        """
        Subscribes to the specified PubSub subscription
        and pull the messages from subscription asynchronously
        """
        streaming_pull = self._subscriber.subscribe(
            await_callbacks_on_shutdown=False,
            subscription=self.subscription,
            scheduler=ThreadScheduler(
                executor=ThreadPoolExecutor(
                    max_workers=self._max_threads_workers,
                    thread_name_prefix="Subscriber_Thread",
                )
            ),
            callback=self.callback,
        )
        self._logger.info(f"Listening for messages on '{self.subscription}'..")
        self._logger.debug(f"Messages redelivering on error: {self.redeliver_messages}")
        self._logger.debug(f"Max Workers in ThreadPool: {self._max_threads_workers}")

        with self._subscriber:
            try:
                # blocks the current thread until the streaming pull is closed
                streaming_pull.result()
            except SubscriberStopError as exc:
                self._logger.error(f"Stopped by Error: {exc}")
                streaming_pull.cancel()

    def _process_message_with_no_redelivering(self, message: pubsub_message.Message):
        """
        This callback should be used ONLY when a message missing is NOT important
        """
        # make the message acknowledgement right after
        # the message has been received to avoid redelivering

        message.ack()
        result = self._process_message(message)
        self._postprocessing(result=result)

    def _process_message(
        self, message: pubsub_message.Message
    ) -> tuple[str, str] | None:
        """
        Single message processing,
        runs in separate thread
        """
        message_data = json.loads(message.data.decode(encoding="utf-8"))
        return self._processor.start_processing(message_data)

    def _postprocessing(self, result: tuple[str, str] | None):
        if isinstance(result, Exception):
            self._logger.warning("Calculation was FAILED: message is SKIPPED")

    def _process_message_with_redelivering_on_error(
        self, message: pubsub_message.Message
    ):
        """
        This callback should be used when we need to REDELIVER
        the message on failed processing
        """

        result = self._process_message(message)
        self._postprocessing(result=result)

        # for redeliver the message on error need to sent 'no acknowledged'
        # explicitly if message processing was failed or 'acknowledge'
        # the message if it was processed correctly
        if not result:
            message.nack()
            return
        message.ack()
