from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def hello_world():
    """
    Hello world endpoint
    """
    return {"msg": "Hello, world!"}
