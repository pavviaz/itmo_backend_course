from fastapi.testclient import TestClient
import pytest
import aiohttp

from app.main import app as app_api


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "uname_inp, passwd1, passwd2, email, expected_result",
    [
        ("test_user0", "123456", "123456", "abc@google.com", "ok"),
        ("test_user0", "123456", "123456", "abc@google.com", "error"),
        ("test_user1", "123456", "1234567", "abc@google.com", "error"),
        ("test_user2", "123456", "123456", "@google.com", "error"),
        ("test_user3", "1", "1", "abc@google.com", "error"),
        ("test_user3", "123456", "123456", "abc@google.com", "ok"),
    ],
)
async def test_register(uname_inp, passwd1, passwd2, email, expected_result):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://0.0.0.0:8001/register",
            json={
                "username": uname_inp,
                "password_1": passwd1,
                "password_2": passwd2,
                "email": email,
            },
        ) as resp:
            responce_code = resp.status

    status = "error"
    if responce_code == 200 or responce_code == 201:
        status = "ok"

    print(responce_code)
    assert status == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "uname, passwd, expected_result",
    [
        ("test_user0", "123456", "ok"),
        ("test_user0", "1234567", "error"),
        ("test_user1", "123456", "error"),
        ("test_user3", "1", "error"),
        ("test_user3", "123456", "ok"),
    ],
)
async def test_register(uname, passwd, expected_result):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://0.0.0.0:8001/login",
            json={
                "username": uname,
                "password": passwd,
            },
        ) as resp:
            responce_code = resp.status

    status = "error"
    if responce_code == 200 or responce_code == 201:
        status = "ok"

    print(responce_code)
    assert status == expected_result
