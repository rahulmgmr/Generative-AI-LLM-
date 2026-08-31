from src.evaluators.correctness import evaluate_correctness


def test_correct_answer():
    expected = "New Delhi"
    response = "New Delhi"

    score = evaluate_correctness(expected, response)

    assert score == 1.0


def test_answer_containing_expected_words():
    expected = "New Delhi"
    response = "New Delhi is the capital of India."

    score = evaluate_correctness(expected, response)

    assert score == 1.0


def test_correct_answer_is_case_insensitive():
    score = evaluate_correctness("New Delhi", "new delhi")

    assert score == 1.0


def test_incorrect_answer():
    expected = "New Delhi"
    response = "Mumbai"

    score = evaluate_correctness(expected, response)

    assert score == 0.0


def test_partially_correct_answer():
    score = evaluate_correctness("New Delhi India", "New Delhi")

    assert score == 2 / 3
