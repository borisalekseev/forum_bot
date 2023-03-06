from dataclasses import dataclass
import datetime


@dataclass
class PostInfo:
    text: str
    photo: list[str]
    times: list[datetime.time]
    duration: int
    topics: str
