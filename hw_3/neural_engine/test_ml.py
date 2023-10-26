import pytest

from model_loader import get_sentiment


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
