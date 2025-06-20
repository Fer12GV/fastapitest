from fastapi import APIRouter, HTTPException
from app.schemas.request_response import AskRequest, AskResponse
from app.services.chatbot_service import ask_openai
from sqlmodel import Session, select
from app.database import engine
from app.models.message import Message

router = APIRouter()


@router.post("/ask", response_model=AskResponse, tags=["Chatbot"])
def ask_question(request: AskRequest):
    """ Endpoint to ask the chatbot a question """
    try:
        response = ask_openai(request.username, request.message)
        return AskResponse(username=request.username, question=request.message, response=response)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{username}", tags=["Chatbot"])
def get_history(username: str):
    """ Endpoint to consult a user's history """
    try:
        with Session(engine) as session:
            messages = session.exec(select(Message).where(Message.username == username)).all()
            return [{"question": msg.question, "response": msg.response} for msg in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
