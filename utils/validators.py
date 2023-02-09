import re
from datetime import time


class TimeValidationError(ValueError):
    pass


def validate_time(times: list[str]) -> list[time]:
    result: list[time] = []
    for time_data in times:
        hours, minutes = map(int, time_data.split(':'))
        if not (0 <= hours < 24 or 0 <= minutes < 60):
            raise ValidationError
        result.append(time(hour=hours, minute=minutes))
    return result
