from dataclasses import dataclass


@dataclass
class AiResponse:
    text: str
    usage: int
