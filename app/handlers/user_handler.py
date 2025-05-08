from fastapi import APIRouter, Depends, Response
from typing import Annotated
from app.services import UserService
from app.dependencies import get_user_service
from app.schemas import UserLoginSchema

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/create_user")
async def create_user(
        response: Response,
        data: UserLoginSchema,
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> dict:
    """
    Создать нового пользователя.
    """
    user_data = await user_service.create_user(response, data)
    return {"user": user_data}