from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    id: int
    title: str
    content: str
    author: str
    date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    belongs_to: int