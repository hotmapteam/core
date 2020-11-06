from dataclasses import dataclass


@dataclass
class Message:
    ts: int
    text: str
    channel: str
    location: tuple
    address: str
