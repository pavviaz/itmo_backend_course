from fastapi import APIRouter

from app.shop import contracts

router = APIRouter(prefix="/shop")


@router.get("/")
def read_root():
    """
    Returns a JSON response with a key-value pair where
    the key is "root_page" and the value is "shop".
    """
    return {"root_page": "shop"}


@router.get("/items/{item_id}")
async def read_item(item_id: int, short: bool | None = None, rank: bool | None = None):
    """
    Retrieve information about an item.

    Args:
        item_id (int): The ID of the item to retrieve information for.
        short (bool, optional): If True, only a short description of the item will be 
        included in the output. Default is None.
        rank (bool, optional): If True, the item's rank will be included in the output. 
        Default is None.

    Returns:
        dict: A dictionary containing the item_id and, depending on the values of short 
        and rank, may also include a description and rank for the item.
    """
    item = {"item_id": item_id}

    if not short:
        item.update({"description": "Best item in the world!"})

    if rank:
        item.update({"rank": 5})

    return item


@router.post("/items/")
async def create_item(item: contracts.Item):
    """
    Create an item in a shop.

    Args:
        item (contracts.Item): An instance of the contracts.Item class representing
        the item to be created.

    Returns:
        dict: A dictionary representation of the item, including the
        price_with_tax key-value pair if applicable.
    """
    item_dict = item.model_dump()

    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
