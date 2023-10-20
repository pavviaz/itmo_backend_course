from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient

from api.app.main import app as app_api
from auth.app.main import app as app_auth
from neural_engine.model_loader import get_sentiment
from auth.app.aservice.contracts import UserRegister


client_api = TestClient(app_api)
client_auth = TestClient(app_auth)


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("Этот город самый лучший город на Земле!", "positive"),
        ("Этот город самый худший город на Земле!", "negative"),
        ("This city is the best city on Earth!", "positive"),
        ("This city is the worst city on Earth!", "negative"),
        ("Этот город просто обычный город на Земле.", "neutral"),
        ("This city is just a typical city on Earth.", "neutral"),
    ],
)
def test_neural_net(text, expected_result):
    try:
        res = get_sentiment(text)
    except Exception:
        res = "error"

    assert res == expected_result


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "uname_inp, passwd1, passwd2, email, expected_result",
#     [
#         ("test_user0", "123456", "123456", "abc@google.com", "ok"),
#         ("test_user0", "123456", "123456", "abc@google.com", "error"),
#         ("test_user1", "123456", "123456", "abc@google.com", "error"),
#         ("test_user4", "123456", "123456", "abc@google.com", "ok"),
#     ],
# )
# async def test_register(uname_inp, passwd1, passwd2, email, expected_result):
#     async with AsyncClient(app=app_api, base_url="http://test") as ac:
#         response = await ac.post(
#             "/register",
#             json={
#                 "username": uname_inp,
#                 "password_1": passwd1,
#                 "password_2": passwd2,
#                 "email": email,
#             },
#         )

#     return responce

#     s = await anext(get_async_session())

#     await add_user(s, **{"username": uname_inp, "hpasswd": passwd, "email": email})
#     res = await get_user(s, uname_output)

#     status = "error"
#     if res:
#         status = "ok"

#     await s.aclose()

#     assert status == expected_result


# # ------------------------------


# @pytest.mark.parametrize(
#     "user_data, expected_result",
#     [
#         (
#             {
#                 "username": "abc1",
#                 "password_1": "123456789",
#                 "password_2": "123456789",
#                 "email": "aaa@google.com",
#             },
#             "ok",
#         ),
#         (
#             {
#                 "username": "abc2",
#                 "password_1": "123",
#                 "password_2": "123",
#                 "email": "aaa@google.com",
#             },
#             "error",
#         ),
#         (
#             {
#                 "username": "abc3",
#                 "password_1": "123456789",
#                 "password_2": "123",
#                 "email": "aaa@google.com",
#             },
#             "error",
#         ),
#         (
#             {
#                 "username": "abc4",
#                 "password_1": "",
#                 "password_2": "123",
#                 "email": "aaa@google.com",
#             },
#             "error",
#         ),
#         (
#             {
#                 "username": "abc5",
#                 "password_1": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
#                 "password_2": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
#                 "email": "aaa@google.com",
#             },
#             "error",
#         ),
#         (
#             {
#                 "username": "abc6",
#                 "password_1": "123456789",
#                 "password_2": "123456789",
#                 "email": "efwwefefw",
#             },
#             "error",
#         ),
#     ],
# )
# def test_user_register(user_data, expected_result):
#     """
#     Test function for user registration.

#     Args:
#         user_data (dict): A dictionary containing the user data,
#         including the username, password_1, password_2, and email.
#         expected_result (str): The expected result of registering
#         the user, which can be either "ok" or "error".

#     Returns:
#         None. The function only performs assertions to
#         check if the result matches the expected result.
#     """
#     try:
#         UserRegister(**user_data)
#         res = "ok"
#     except Exception:
#         res = "error"

#     assert res == expected_result


# def test_register():
#     response = client.post(
#         "/auth/register",
#         json={
#             "username": "test2_1",
#             "password_1": "123456789",
#             "password_2": "123456789",
#             "email": "aaa@google.com",
#         },
#     )
#     assert response.status_code == 201


# def test_login():
#     response = client.post(
#         "/auth/login",
#         json={"username": "test2_1", "password": "123456789"},
#     )
#     assert response.status_code == 200


# def test_get_info():
#     response = client.post(
#         "/auth/login",
#         json={"username": "test2_1", "password": "123456789"},
#     )
#     token = response.json()["access_token"]

#     response = client.post(
#         "/auth/profile",
#         json={
#             "token": token,
#         },
#     )
#     assert response.status_code == 200
