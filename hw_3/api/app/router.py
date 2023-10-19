import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
import aiohttp

from app.contracts import UserRegister, UserLogin, Token


router = APIRouter(prefix="/service", tags=["service"])


@router.post("/register")
async def register(user_data: UserRegister):
    """
    Register a new user via 'auth' service

    Args:
        user_data (UserRegister): The user registration data
        including the username, password, and email.

    Returns:
        JSONResponse: A response with a status code of
        201 indicating that the user has been created.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{os.getenv('AUTH_IP', 'http://localhost:8001/')}auth/register", json=user_data) as resp:
            # return await resp
            responce = await resp.json()
    
    return responce


@router.post("/login")
async def login(user_data: UserLogin):
    """
    Authenticates a user and generates an access token.

    Args:
        user_data (UserLogin): A UserLogin object containing
        the user's login credentials (username and password).

    Returns:
        dict: A dictionary containing the access token.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{os.getenv('AUTH_IP')}/login", json=user_data) as resp:
            # return await resp
            responce = await resp.json()
    
    return responce

    return {"access_token": token}


@router.post("/profile")
async def get_user_data(
    token: Token, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieves user data based on a provided access token.

    Args:
        token (Token): The access token provided by the client.
        session (AsyncSession, optional): The asynchronous database session.
        Defaults to the result of calling the `get_async_session` function.

    Returns:
        The user data retrieved based on the provided access token.
    """
    username = validate_access_token(token=token.token)
    user = await get_user(session=session, username=username)

    return user
