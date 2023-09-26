from fastapi import APIRouter

from app.user import contracts

router = APIRouter(prefix="/users")


@router.get("/")
def read_root():
    """
    Returns a JSON response with a key-value pair where
    the key is "root_page" and the value is "user".
    """
    return {"root_page": "user"}


@router.get("/{user_id}")
async def read_user(user_id: str):
    """
    Retrieves a user by their ID and returns a JSON response.

    Args:
        user_id (str): The ID of the user to be retrieved.

    Returns:
        dict: A JSON response containing the user ID.
    """
    return {"item_id": user_id}


@router.post("/register")
async def register_user(user_info: contracts.UserRegister):
    """
    Handles a POST request to the "/register" endpoint.

    Args:
        user_info (contracts.UserRegister): A UserRegister object
        containing the user's information.

    Returns:
        item_dict: A dictionary containing the user's information and status.
    """
    item_dict = user_info.model_dump()

    item_dict.update(
        {"status": f"user {user_info.name} has been successfully registered"}
    )
    return item_dict


@router.post("/login")
async def login_user(user_info: contracts.UserLogin):
    """
    Handles a POST request to the "/login" endpoint.

    Args:
        user_info (contracts.UserLogin): An object containing the user information.

    Returns:
        item_dict: A dictionary containing the user information and a "status"
        key indicating the success of the login operation.
    """
    item_dict = user_info.model_dump()

    item_dict.update(
        {"status": f"user {user_info.name} has been successfully logged in"}
    )
    return item_dict
