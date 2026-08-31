# AI LLM Evaluation Framework

This project evaluates answers produced by a locally running Ollama model. It reads questions from a JSON file, asks the model for an answer, scores that answer, and saves a report.

## Framework structure

```text
config/
  config.yaml              Score thresholds used for PASS or FAIL
  config_loader.py         Reads the threshold configuration

data/
  test_cases.json          Questions, contexts, and expected answers

src/
  llm/llm_client.py        Sends each question to the local Ollama model
  evaluators/              Contains one evaluator for each score
    correctness.py
    grounding.py
    hallucination.py
    toxicity.py
  metrics/metrics.py       Calculates average scores
  run_evaluation.py        Runs the complete evaluation flow

tests/
  test_correctness.py      Tests correctness-score logic
  test_grounding.py        Tests grounding-score logic
  test_hallucination.py    Tests hallucination-score logic
  test_toxicity.py         Tests toxicity-score logic
  test_test_cases.py       Checks that the JSON test data is valid

reports/
  evaluation_results.json  Generated evaluation report
```

## How one evaluation run works

1. `src/run_evaluation.py` reads all entries from `data/test_cases.json`.
2. For each entry, `src/llm/llm_client.py` sends its `question` and `context` to Ollama.
3. Your local model (`qwen3-vl:2b`) generates a real answer.
4. The answer is evaluated by the files in `src/evaluators/`.
5. The scores are compared with thresholds in `config/config.yaml`.
6. The final details and overall PASS/FAIL result are saved to `reports/evaluation_results.json`.

The evaluation run always uses real answers from your local Ollama model. It does not use mocked or dummy model responses.

## Test-case format

Add evaluation scenarios in `data/test_cases.json` using this format:

```json
{
  "id": "TC006",
  "question": "What is the capital of France?",
  "context": "Paris is the capital of France.",
  "expected_answer": "Paris"
}
```

Each test case must have a unique `id`, `question`, `context`, and `expected_answer`.

## Setup

Open PowerShell in the project folder, then install the Python packages:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Ollama must be installed and running locally. This framework is configured to use `qwen3-vl:2b` in `src/llm/llm_client.py`.

Download the model once if it is not already available:

```powershell
ollama pull qwen3-vl:2b
```

You can confirm that it is available with:

```powershell
ollama list
```

## Trigger an automated evaluation run

Run this command from the project folder:

```powershell
.\.venv\Scripts\python.exe -m src.run_evaluation
```

This automatically evaluates every JSON test case and overwrites `reports/evaluation_results.json` with the latest results.

The terminal prints the final overall status:

```text
Overall Status: PASS
```

or:

```text
Overall Status: FAIL
```

## Run evaluator tests

These tests check the scoring logic and JSON test-case format. They do not call Ollama.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Change evaluation thresholds

Edit `config/config.yaml` when you want to change the score needed for PASS.

- `correctness` and `grounding`: higher score is better.
- `hallucination` and `toxicity`: lower score is better.

For example, `correctness: 0.80` means the average correctness score must be at least `0.80` for the overall result to pass.
