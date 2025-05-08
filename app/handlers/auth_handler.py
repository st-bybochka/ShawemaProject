from fastapi import APIRouter, Depends, Response, Request
from typing import Annotated
from app.schemas import UserLoginSchema
from app.services import AuthService
from app.dependencies import get_auth_service, get_current_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
        response: Response,
        data: UserLoginSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:

    tokens = await auth_service.login(data, response)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }


@router.post("/logout")
async def logout(

        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        token: str = Depends(get_current_token),

):

    await auth_service.logout(token)
    return {"success": True, "message": "Вы успешно вышли из системы"}



@router.get("/refresh")
async def refresh(
        request: Request,
        response: Response,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:

    tokens = await auth_service.refresh_access_token(request, response)
    return tokens