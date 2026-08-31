import json
from pathlib import Path

from src.evaluators.correctness import evaluate_correctness
from src.evaluators.grounding import evaluate_grounding
from src.evaluators.hallucination import evaluate_hallucination
from src.evaluators.toxicity import evaluate_toxicity
from src.metrics.metrics import calculate_average_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEST_CASES_PATH = PROJECT_ROOT / "data" / "test_cases.json"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_results.json"


def load_test_cases(path=DEFAULT_TEST_CASES_PATH):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_status(score, threshold, higher_is_better=True):
    passes = score >= threshold if higher_is_better else score <= threshold
    return "PASS" if passes else "FAIL"


def evaluate_test_case(test_case, thresholds, response_generator):
    question = test_case["question"]
    context = test_case["context"]
    expected_answer = test_case["expected_answer"]
    response = response_generator(question, context)

    correctness_score = evaluate_correctness(expected_answer, response)
    grounding_score = evaluate_grounding(context, response)
    hallucination_score = evaluate_hallucination(grounding_score)
    toxicity_result = evaluate_toxicity(response)
    toxicity_score = toxicity_result["toxicity_score"]

    return {
        "test_case_id": test_case["id"],
        "question": question,
        "context": context,
        "expected_answer": expected_answer,
        "model_response": response,
        "correctness": {
            "score": correctness_score,
            "status": get_status(correctness_score, thresholds["correctness"]),
        },
        "grounding": {
            "score": grounding_score,
            "status": get_status(grounding_score, thresholds["grounding"]),
        },
        "hallucination": {
            "score": hallucination_score,
            "status": get_status(
                hallucination_score,
                thresholds["hallucination"],
                higher_is_better=False,
            ),
        },
        "toxicity": {
            "score": toxicity_score,
            "status": get_status(
                toxicity_score,
                thresholds["toxicity"],
                higher_is_better=False,
            ),
            "detected_words": toxicity_result["detected_words"],
        },
    }


def run_evaluation(test_cases=None, thresholds=None, response_generator=None):
    if thresholds is None:
        from config.config_loader import load_config

        thresholds = load_config()["thresholds"]
    if test_cases is None:
        test_cases = load_test_cases()
    if response_generator is None:
        from src.llm.llm_client import generate_response

        response_generator = generate_response

    results = [
        evaluate_test_case(test_case, thresholds, response_generator)
        for test_case in test_cases
    ]

    overall_results = {
        "correctness": calculate_average_score(
            [result["correctness"]["score"] for result in results]
        ),
        "grounding": calculate_average_score(
            [result["grounding"]["score"] for result in results]
        ),
        "hallucination": calculate_average_score(
            [result["hallucination"]["score"] for result in results]
        ),
        "toxicity": calculate_average_score(
            [result["toxicity"]["score"] for result in results]
        ),
    }
    overall_results["overall_status"] = (
        "PASS"
        if (
            overall_results["correctness"] >= thresholds["correctness"]
            and overall_results["grounding"] >= thresholds["grounding"]
            and overall_results["hallucination"] <= thresholds["hallucination"]
            and overall_results["toxicity"] <= thresholds["toxicity"]
        )
        else "FAIL"
    )

    return {
        "thresholds": thresholds,
        "overall_results": overall_results,
        "test_results": results,
    }


def save_report(report, path=DEFAULT_REPORT_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def main():
    report = run_evaluation()
    save_report(report)
    print("Overall Status:", report["overall_results"]["overall_status"])


if __name__ == "__main__":
    main()
