def evaluate_grounding(context, model_response):

    context_words = set(context.lower().split())
    response_words = set(model_response.lower().split())

    common_words = context_words.intersection(response_words)

    if len(response_words) == 0:
        return 0.0

    score = len(common_words) / len(response_words)

    return score