import os

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi import status
import aiohttp

from app.contracts import UserRegister, UserLogin, UserRequest


router = APIRouter(tags=["service"])


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
    user_data_json = user_data.model_dump()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{os.getenv('AUTH_IP', 'http://0.0.0.0:8001')}/register",
            json=user_data_json,
        ) as resp:
            responce = await resp.json()

    return responce


@router.post("/login")
async def login(user_data: UserLogin):
    """
    Authenticates a user and generates an access token via 'auth' service.

    Args:
        user_data (UserLogin): A UserLogin object containing
        the user's login credentials (username and password).

    Returns:
        dict: A dictionary containing the access token.
    """
    user_data_json = user_data.model_dump()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{os.getenv('AUTH_IP', 'http://0.0.0.0:8001')}/login",
            json=user_data_json,
        ) as resp:
            responce = await resp.json()

    return responce


@router.post("/classify")
async def classify(user_data: UserRequest):
    """
    Classify user data by sending it to two different endpoints ('auth' and 'neural_engine') 
    and returning the response from the second endpoint.

    Args:
        user_data (UserRequest): An instance of the UserRequest class 
        that contains the user's text and token.

    Returns:
        The response from the second endpoint.
    """
    user_data_json = user_data.model_dump()
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{os.getenv('AUTH_IP', 'http://0.0.0.0:8001')}/profile",
            json=user_data_json,
        ) as resp:
            responce_code = resp.status

    if responce_code != status.HTTP_200_OK:
        return JSONResponse(status_code=responce_code, content={"msg": "Bad token"})

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{os.getenv('ML_IP', 'http://0.0.0.0:8002')}/classify?user_q={user_data.text}",
        ) as resp:
            responce = await resp.json()

    return responce
