import httpx
from httpx import HTTPStatusError
from sqlmodel import Session, select
from app.models.message import Message
from app.models.user import User
from app.database import engine
from app.config import OPENAI_API_KEY, OPENAI_API_URL


def ask_openai(username: str, question: str) -> str:
    try:
        with Session(engine) as session:
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

        response = httpx.post(OPENAI_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]

        with Session(engine) as session:
            msg = Message(username=username, question=question, response=content)
            session.add(msg)
            session.commit()

        return content
    except (HTTPStatusError, httpx.RequestError):
        raise ValueError("User not found")
    except Exception:
        raise ValueError("User not found")
