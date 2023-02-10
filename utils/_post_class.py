from dataclasses import dataclass
import datetime


@dataclass
class PostInfo:
    text: str
    photos: list[str]
    times: list[datetime.time]
    duration: int
