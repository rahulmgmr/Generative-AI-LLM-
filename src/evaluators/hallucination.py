def evaluate_hallucination(grounding_score):
    """
    Estimate hallucination based on the grounding score.

    Higher grounding means lower hallucination.
    """

    hallucination_score = 1.0 - grounding_score

    return hallucination_score