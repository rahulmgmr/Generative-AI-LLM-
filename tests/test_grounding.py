from src.evaluators.grounding import evaluate_grounding


def test_fully_grounded_response():
    context = "Jupiter is the largest planet"
    response = "Jupiter is the largest planet"

    assert evaluate_grounding(context, response) == 1.0


def test_partially_grounded_response():
    context = "Jupiter is the largest planet"
    response = "Jupiter is the largest planet discovered yesterday"

    assert evaluate_grounding(context, response) == 5 / 7


def test_ungrounded_response():
    context = "Jupiter is the largest planet"
    response = "Saturn has rings"

    assert evaluate_grounding(context, response) == 0.0


def test_empty_response_is_not_grounded():
    assert evaluate_grounding("Jupiter is the largest planet", "") == 0.0
