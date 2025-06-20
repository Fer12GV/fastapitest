# app/services/chatbot_service.py

import httpx
from sqlmodel import Session, select
from app.models.message import Message
from app.models.user import User
from app.database import engine
from app.config import OPENAI_API_KEY, OPENAI_API_URL


def ask_openai(username: str, question: str) -> str:
    """ Service to send a question to the OpenAI API and save it to the database"""
    with Session(engine) as session:
        """ Log in to the database """
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise ValueError("User not found")

        user_role = user.role

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are {user_role}."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = httpx.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        with Session(engine) as session:
            """ Save the interaction to the database """
            msg = Message(username=username, question=question, response=content)
            session.add(msg)
            session.commit()

        return content

    except Exception as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {str(e)}")
