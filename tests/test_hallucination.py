from src.evaluators.hallucination import evaluate_hallucination


def test_fully_grounded_response_has_no_hallucination():
    assert evaluate_hallucination(1.0) == 0.0


def test_ungrounded_response_has_full_hallucination():
    assert evaluate_hallucination(0.0) == 1.0


def test_hallucination_is_inverse_of_grounding():
    assert evaluate_hallucination(0.65) == 0.35
