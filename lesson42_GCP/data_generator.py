import json
from typing import Generator
from lesson42_GCP.publisher import Publisher


class DataGenerator:

    def __init__(self, google_project: str, topic: str):
        self._publisher = Publisher(
            google_cloud_project=google_project,
        )
        self._topic = topic
        self.threshold = 100
        self._cases = (
            (
                [],
                3,
                []
            ),
            (
                [1],
                1,
                [1]
            ),
            (
                [1, 1, 1, 1, 1, 1, 2],
                3,
                [1, 1, 1, 1, 2]
            ),
            (
                [1, 3, 2, 4, 0, 5],
                2,
                [3, 3, 4, 4, 5]
            ),
            (
                [1, 3, -1, -3, 5, 3, 6, 7],
                3,
                [3, 3, 5, 5, 6, 7]
            ),
            (
                [1, 3, 2, 9, 2, 0, 7, 5, 1, 1, 4, 6, 6, 5, 8, 7, 8],
                5,
                [9, 9, 9, 9, 7, 7, 7, 6, 6, 6, 8, 8, 8]
            )
        )
        self._iterator = self._generate_cases()

    def _generate_cases(self) -> Generator[tuple[list[int], int, list[int]], None, None]:
        counter = 0

        while counter <= self.threshold:
            for case in self._cases:
                yield case

            counter += 1

    def _generate_batches(self):
        counter = 0
        batches = []
        while counter <= len(self._cases):
            nums, k, expected = yield from self._iterator
            batch_data = {
                'nums': nums,
                'k': k,
                'expected': expected
            }
            batches.append(
                json.dumps(batch_data)
            )
            counter += 1

        return batches

    def push_item(self):
        self._publisher.publish_many(
            messages=self._generate_batches(),
            topic_id=self._topic,
            timeout=10
        )



