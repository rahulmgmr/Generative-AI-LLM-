from src.run_evaluation import load_test_cases


REQUIRED_FIELDS = {"id", "question", "context", "expected_answer"}


def test_test_cases_have_required_fields_and_unique_ids():
    test_cases = load_test_cases()
    ids = []

    for test_case in test_cases:
        assert REQUIRED_FIELDS.issubset(test_case)
        assert all(
            isinstance(test_case[field], str) and test_case[field].strip()
            for field in REQUIRED_FIELDS
        )
        ids.append(test_case["id"])

    assert len(ids) == len(set(ids))
