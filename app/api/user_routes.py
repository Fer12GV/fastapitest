from fastapi import APIRouter

router = APIRouter()

from fastapi import APIRouter, HTTPException
from app.schemas.request_response import InitUserRequest
from app.services.user_service import create_user

router = APIRouter()


@router.post("/init_user", tags=["User Management"])
def init_user(request: InitUserRequest):
    try:
        user, status = create_user(request.username, request.role)
        if status == "updated":
            return {"message": f"User '{user.username}' updated with new role '{user.role}'."}
        return {"message": f"User '{user.username}' with role '{user.role}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
