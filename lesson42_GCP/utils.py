import collections
from datetime import date, datetime, timedelta, timezone


UTC_TIMEZONE = timezone.utc
DATETIME_STR_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def get_current_datetime_str(
    time_zone: timezone = UTC_TIMEZONE, fmt: str = DATETIME_STR_FORMAT
) -> str:
    return datetime.now(tz=time_zone).strftime(fmt)


def find_sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    left = right = 0
    queue = collections.deque()
    result = []

    while right < len(nums):
        while queue and nums[queue[-1]] < nums[right]:
            queue.pop()

        queue.append(right)

        if left > queue[0]:
            queue.popleft()

        if right - left >= k - 1:
            result.append(nums[queue[0]])
            left += 1

        right += 1

    return result
