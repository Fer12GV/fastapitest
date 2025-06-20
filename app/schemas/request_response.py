from pydantic import BaseModel, Field


class InitUserRequest(BaseModel):
    """ Schema to initialize a user """
    username: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)


class AskRequest(BaseModel):
    """ Schema for sending questions to the chatbot """
    username: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class AskResponse(BaseModel):
    """ Chatbot response scheme """
    username: str
    question: str
    response: str
