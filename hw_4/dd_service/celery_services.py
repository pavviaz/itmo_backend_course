import os

from scidownl import scihub_download
from celery import Celery
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


DOI_URL = "https://doi.org/"
SAVE_SENTIMENT = "sent.txt"


celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

model_checkpoint = "cointegrated/rubert-tiny-sentiment-balanced"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)


@celery.task(name="download_doi")
def download_article(full_doi: str):
    """
    Downloads an article from a scientific
    database using its DOI (Digital Object Identifier).

    Args:
        full_doi (str): The full DOI of the
        article to be downloaded.

    Returns:
        None. The function downloads the article and
        saves it as a PDF file in the specified download directory.
    """
    prefix, doi = full_doi.split("/")
    download_dir = os.path.join(os.getenv("DOI_DOWNLOAD_PATH"), prefix)
    os.makedirs(download_dir, exist_ok=True)

    filename = os.path.join(download_dir, f"{prefix}_{doi}.pdf")

    scihub_download(keyword=f"{DOI_URL}{full_doi}", paper_type="doi", out=filename)


@celery.task(name="get_sentiment")
def download_article(text: str):
    """
    Perform sentiment analysis on the input text using
    a pre-trained model and save the sentiment result to a file.

    Args:
        text (str): The input text for sentiment analysis.

    Returns:
        None: The function does not return any value.
        It saves the sentiment result to a file.
    """
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(
            model.device
        )
        proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()[0]

    res = model.config.id2label[proba.argmax()]

    with open(SAVE_SENTIMENT, "a+") as f:
        f.write(f"{text} --> {res}\n")
