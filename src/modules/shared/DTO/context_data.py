from dataclasses import dataclass
from datetime import datetime
@dataclass
class ContextDTO:
    id: str = None
    tags: list = None
    convo_id: str = None
    user_id: str = None
    conversation_date: datetime = datetime.now()
    last_updated: datetime = datetime.now()
    last_mentioned: datetime = datetime.now()
    status: int = 1
