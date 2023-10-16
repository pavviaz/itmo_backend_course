from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest

from app.main import app
from app.database import get_async_session
from app.auth.auth import create_access_token, validate_access_token
from app.auth.contracts import UserRegister
from app.auth.models import User
from app.database import Base, engine
from app.auth.dao import get_user, add_user


client = TestClient(app)


@pytest.mark.parametrize(
    "token, expected_result",
    [
        (create_access_token({"sub": "test"}), "test"),
        (create_access_token({"sub": "test123"}), "test123"),
        (create_access_token({"sub": "test"}) + "AAAA", "401"),
        (create_access_token({"sub": "test"})[:-1], "401"),
        (create_access_token({"sub": "test"})[1:], "401"),
        ("", "401"),
    ],
)
def test_validate_access_token(token, expected_result):
    """
    Test function for validating the access token.

    Args:
        token (str): The access token to be validated.
        expected_result (str): The expected result of the validation.

    Returns:
        None
    """
    try:
        res = validate_access_token(token)
    except HTTPException:
        res = "401"

    assert res == expected_result


@pytest.mark.parametrize(
    "user_data, expected_result",
    [
        (
            {
                "username": "abc1",
                "password_1": "123456789",
                "password_2": "123456789",
                "email": "aaa@google.com",
            },
            "ok",
        ),
        (
            {
                "username": "abc2",
                "password_1": "123",
                "password_2": "123",
                "email": "aaa@google.com",
            },
            "error",
        ),
        (
            {
                "username": "abc3",
                "password_1": "123456789",
                "password_2": "123",
                "email": "aaa@google.com",
            },
            "error",
        ),
        (
            {
                "username": "abc4",
                "password_1": "",
                "password_2": "123",
                "email": "aaa@google.com",
            },
            "error",
        ),
        (
            {
                "username": "abc5",
                "password_1": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "password_2": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "email": "aaa@google.com",
            },
            "error",
        ),
        (
            {
                "username": "abc6",
                "password_1": "123456789",
                "password_2": "123456789",
                "email": "efwwefefw",
            },
            "error",
        ),
    ],
)
def test_user_register(user_data, expected_result):
    """
    Test function for user registration.

    Args:
        user_data (dict): A dictionary containing the user data,
        including the username, password_1, password_2, and email.
        expected_result (str): The expected result of registering
        the user, which can be either "ok" or "error".

    Returns:
        None. The function only performs assertions to
        check if the result matches the expected result.
    """
    try:
        UserRegister(**user_data)
        res = "ok"
    except Exception:
        res = "error"

    assert res == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "uname_inp, passwd, email, uname_output, expected_result",
    [
        ("test_user0", "123456", "abc@google.com", "test_user0", "ok"),
        ("test_user1", "123456", "abc@google.com", "test_user0", "error"),
        ("test_user3", "123456", "abc@google.com", "test_user4", "error"),
        ("test_user4", "123456", "abc@google.com", "test_user4", "ok"),
    ],
)
async def test_get_user(uname_inp, passwd, email, uname_output, expected_result):
    """
    Test function for the get_user function from the app.auth.dao module.

    Args:
        uname_inp (str): The input username for adding a user to the database.
        passwd (str): The password for adding a user to the database.
        email (str): The email for adding a user to the database.
        uname_output (str): The username to retrieve from the database.
        expected_result (str): The expected result of the test, either "ok" or "error".

    Returns:
        None. The function does not return any value. The test result is determined
        by the assertion at the end of the function.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        pass

    s = await anext(get_async_session())

    await add_user(s, **{"username": uname_inp, "hpasswd": passwd, "email": email})
    res = await get_user(s, uname_output)

    status = "error"
    if res:
        status = "ok"

    await s.aclose()

    assert status == expected_result


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "username": "test2_1",
            "password_1": "123456789",
            "password_2": "123456789",
            "email": "aaa@google.com",
        },
    )
    assert response.status_code == 201


def test_login():
    response = client.post(
        "/auth/login",
        json={"username": "test2_1", "password": "123456789"},
    )
    assert response.status_code == 200


def test_get_info():
    response = client.post(
        "/auth/login",
        json={"username": "test2_1", "password": "123456789"},
    )
    token = response.json()["access_token"]

    response = client.post(
        "/auth/profile",
        json={
            "token": token,
        },
    )
    assert response.status_code == 200
