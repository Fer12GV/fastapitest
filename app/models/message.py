from typing import Optional
from sqlmodel import SQLModel, Field


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    question: str
    response: str
