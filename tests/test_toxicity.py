from src.evaluators.toxicity import evaluate_toxicity


def test_safe_response_is_not_toxic():
    result = evaluate_toxicity("I can help you with that.")

    assert result["toxicity_score"] == 0.0
    assert result["is_toxic"] is False
    assert result["detected_words"] == []


def test_toxic_response_is_detected():
    result = evaluate_toxicity("That was a stupid idea.")

    assert result["toxicity_score"] == 1.0
    assert result["is_toxic"] is True
    assert result["detected_words"] == ["stupid"]


def test_multiple_toxic_words_are_reported():
    result = evaluate_toxicity("Do not be an idiot or a moron.")

    assert result["detected_words"] == ["idiot", "moron"]
