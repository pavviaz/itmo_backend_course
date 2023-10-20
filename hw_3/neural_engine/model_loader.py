import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


model_checkpoint = "cointegrated/rubert-tiny-sentiment-balanced"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)

if torch.cuda.is_available():
    model.cuda()


def get_sentiment(text, return_type="label"):
    """Calculate sentiment of a text. `return_type` can be 'label', 'score' or 'proba'"""
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(
            model.device
        )
        proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()[0]
    if return_type == "label":
        return model.config.id2label[proba.argmax()]
    elif return_type == "score":
        return proba.dot([-1, 0, 1])
    return proba


if __name__ == "__main__":
    print(get_sentiment("Этот город самый лучший город на Земле!"))
    print(get_sentiment("Этот город самый худший город на Земле!"))
