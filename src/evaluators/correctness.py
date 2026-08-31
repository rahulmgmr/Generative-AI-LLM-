def evaluate_correctness(expected_answer, model_response):

    expected_words = set(expected_answer.lower().split())
    response_words = set(model_response.lower().split())

    common_words = expected_words.intersection(response_words)

    if len(expected_words) == 0:
        return 0.0

    score = len(common_words) / len(expected_words)

    return score