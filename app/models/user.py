from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """ Table template for the user """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    role: str
