from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from datetime import datetime



class SChat(BaseModel):
    id: int
    last_message_date: Optional[datetime] = None
    create_at:Optional[datetime] = None
    owners: Optional[list] = None
    messages_id: Optional[list] = None

    class Config:
        orm_mode = True


class SMessage(BaseModel):
    message: str

class SMessages(BaseModel):
    id: int
    text: str
    sending_date: datetime
    is_read: bool
    chat_id: int

