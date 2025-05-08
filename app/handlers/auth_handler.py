from fastapi import APIRouter, Depends, Response, Request
from typing import Annotated
from app.schemas import UserLoginSchema
from app.services import AuthService
from app.dependencies import get_auth_service

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
        response: Response,
):

    await auth_service.logout(response)
    return {"message": "Logout successful"}


@router.get("/refresh")
async def refresh(
        request: Request,
        response: Response,
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:

    tokens = await auth_service.refresh_access_token(request, response)
    return tokens