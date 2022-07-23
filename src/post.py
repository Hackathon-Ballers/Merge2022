from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    title: str
    content: str
    author: str
    date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id: int = 0
    belongs_to:any = None