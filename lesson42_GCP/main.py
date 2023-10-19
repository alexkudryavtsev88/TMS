import logging
import sys
import threading
import time

from lesson42_GCP.config import Config
from lesson42_GCP.data_generator import DataGenerator
from lesson42_GCP.subscriber import Subscriber
from lesson42_GCP.processor import Processor


logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
    "[%(name)s:%(funcName)s:%(lineno)s][%(threadName)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    stream=sys.stdout,
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


_CONFIG = Config(
    GOOGLE_PROJECT_ID='alpine-dogfish-402315',
    TOPIC_ID='my-first-topic',
    SUBSCRIPTION_ID='my-first-topic-sub',
    IS_REDELIVER=False
)

# "quota_project_id": "alpine-dogfish-402315"


def run_subscriber():
    def run_in_thread():
        subscriber = Subscriber(
            google_cloud_project=_CONFIG.GOOGLE_PROJECT_ID,
            subscription_id=_CONFIG.SUBSCRIPTION_ID,
            redeliver_message=_CONFIG.IS_REDELIVER,
            processor=Processor()
        )
        return threading.Thread(target=subscriber.run, name="Subscriber_Process")

    run_in_thread().start()


def produce_data():
    gen = DataGenerator(
        google_project=_CONFIG.GOOGLE_PROJECT_ID,
        topic=_CONFIG.TOPIC_ID
    )
    for i in range(20):
        gen.push_item()
        time.sleep(1)


if __name__ == '__main__':
    run_subscriber()
    # time.sleep(1)
    # produce_data()
