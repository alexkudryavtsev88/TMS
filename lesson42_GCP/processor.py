import json
from lesson42_GCP.utils import find_sliding_window_maximum


class Processor:

    @staticmethod
    def start_processing(message: str):
        data = json.loads(message)

        result = find_sliding_window_maximum(
            nums=data["nums"],
            k=data["k"],
        )
        try:
            assert result == data["expected"]
            return result
        except Exception as exc:
            return exc




