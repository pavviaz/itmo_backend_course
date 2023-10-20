from fastapi import APIRouter

from model_loader import get_sentiment


router = APIRouter(tags=["ml"])


@router.get("/classify")
async def classify(user_q: str):    
    return {"class": get_sentiment(user_q)}
