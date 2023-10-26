from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.aservice.contracts import UserLogin, UserRegister, Token
from app.database import get_async_session
from app.aservice.dao import get_user, add_user
from app.aservice.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    validate_access_token,
)


router = APIRouter(tags=["auth"])


@router.post("/register")
async def register(
    user_data: UserRegister, session: AsyncSession = Depends(get_async_session)
):
    """
    Register a new user.

    Args:
        user_data (UserRegister): The user registration data
        including the username, password, and email.
        session (AsyncSession, optional): The async session to use for
        database operations. Defaults to Depends(get_async_session).

    Raises:
        HTTPException: If a user with the same username already exists in the database.

    Returns:
        JSONResponse: A response with a status code of
        201 indicating that the user has been created.
    """
    if await get_user(session=session, username=user_data.username):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="User already exists"
        )

    await add_user(
        session=session,
        username=user_data.username,
        hpasswd=get_password_hash(user_data.password_1),
        email=user_data.email,
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="User has been created"
    )


@router.post("/login")
async def login(
    user_data: UserLogin, session: AsyncSession = Depends(get_async_session)
):
    """
    Authenticates a user and generates an access token.

    Args:
        user_data (UserLogin): A UserLogin object containing
        the user's login credentials (username and password).
        session (AsyncSession, optional): An AsyncSession object for
        database operations. Defaults to Depends(get_async_session).

    Raises:
        HTTPException: Raised if the login or password is incorrect.

    Returns:
        dict: A dictionary containing the access token.
    """
    user = await get_user(session=session, username=user_data.username)
    if not user or not verify_password(user_data.password, user.hpasswd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password",
        )

    token = create_access_token({"sub": user.username})

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
