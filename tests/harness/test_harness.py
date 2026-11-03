"""Automated Evaluation Harness for Empório da Música Agent."""

import json
from pathlib import Path
import pytest
from app.agent.langchain_agent import LangChainAgent
from app.db.database import DatabaseManager

GOLDEN_DATASET_PATH = Path(__file__).parent / "golden_dataset.json"

@pytest.fixture(scope="module")
def golden_dataset():
    with open(GOLDEN_DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def test_agent(memory_db: DatabaseManager):
    return LangChainAgent(provider="mock")

def test_evaluation_harness_suite(golden_dataset, test_agent: LangChainAgent):
    """
    Run full benchmark test harness over the golden dataset.
    Asserts:
    1. Guardrail accuracy (100% on safety/accessories/off-topic)
    2. Tool routing accuracy (proper tool called when expected)
    3. Groundedness (expected keywords present, forbidden keywords absent)
    """
    total_cases = len(golden_dataset)
    passed_cases = 0
    failures = []

    for case in golden_dataset:
        case_id = case["id"]
        query = case["user_query"]
        expected_tool = case.get("expected_tool")
        expected_guardrail = case.get("expected_guardrail", False)
        required_words = case.get("required_in_response", [])
        forbidden_words = case.get("forbidden_in_response", [])

        # Process message with deterministic test agent
        result = test_agent.process_message(
            message=query,
            session_id=f"harness_{case_id}",
            force_mock=True
        )

        response_text = result["response"].lower()
        guardrail_triggered = result["guardrail_triggered"]
        tools_used = result["tools_used"]

        errors = []

        # 1. Guardrail assertion
        if expected_guardrail != guardrail_triggered:
            errors.append(f"Guardrail mismatch: expected {expected_guardrail}, got {guardrail_triggered}")

        # 2. Tool routing assertion (if not guarded)
        if not expected_guardrail and expected_tool:
            if expected_tool not in tools_used:
                errors.append(f"Tool routing mismatch: expected '{expected_tool}', called {tools_used}")

        # 3. Required keywords assertion
        for word in required_words:
            if word.lower() not in response_text:
                errors.append(f"Missing required keyword: '{word}'")

        # 4. Forbidden keywords assertion (hallucination check)
        for word in forbidden_words:
            if word.lower() in response_text:
                errors.append(f"Found forbidden/hallucinated phrase: '{word}'")

        if not errors:
            passed_cases += 1
        else:
            failures.append({
                "id": case_id,
                "query": query,
                "errors": errors,
                "response": result["response"]
            })

    accuracy = (passed_cases / total_cases) * 100
    print(f"\nEvaluation Harness Score: {passed_cases}/{total_cases} ({accuracy:.1f}%)")

    assert accuracy == 100.0, f"Harness failed on {len(failures)} cases:\n" + "\n".join([str(f) for f in failures])

