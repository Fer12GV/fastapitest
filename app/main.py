from fastapi import FastAPI
from app.database import init_db
from app.api import user_routes, chatbot_routes, health_routes


tags_metadata = [
    {
        "name": "User Management",
        "description": "Endpoints related to user creation and role configuration.",
    },
    {
        "name": "Chatbot",
        "description": "Endpoints for interacting with the OpenAI-based chatbot and viewing history.",
    },
    {
        "name": "Health Check",
        "description": "Service and database status verification.",
    }
]

app = FastAPI(
    title="Configurable Chatbot API",
    description="RESTful API using FastAPI and OpenAI to simulate a role-based chatbot.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

init_db()

app.include_router(user_routes.router)
app.include_router(chatbot_routes.router)
app.include_router(health_routes.router)
