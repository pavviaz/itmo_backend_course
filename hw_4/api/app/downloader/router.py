import os
import uuid
import pickle
import json

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi import status
from celery import Celery

from app.downloader.contracts import DownloadingRequest


celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

router = APIRouter(tags=["tasker"])


@router.post("/doi")
async def create_download_task(download_data: DownloadingRequest):
    """
    Handles a POST request to the "/doi" endpoint.
    Creates a task to download a list of DOIs using Celery.

    Args:
        download_data (DownloadingRequest): A request body
        parameter containing a `links_list` field,
        which is a list of DOIs to be downloaded.

    Returns:
        JSONResponse: A JSON response with a status code of
        201 (Created) and a message indicating
        that the task has been created successfully.
    """
    task_ids = {str(uuid.uuid4()): doi for doi in download_data.links_list}

    for uid, d in task_ids.items():
        celery.send_task("download_doi", args=(d,), task_id=uid)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"msg": "Task has been created successfully"},
    )


@router.post("/sentiment")
async def create_download_task(text: str):
    """
    Handles a POST request to the "/sentiment" endpoint.
    Creates a task to get sentiment of a text

    Args:
        text (str): The text for which sentiment
        analysis task needs to be created.

    Returns:
        JSONResponse: A JSON response indicating that
        the task has been created successfully.
    """
    celery.send_task("get_sentiment", args=(text,))

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"msg": "Task has been created successfully"},
    )
