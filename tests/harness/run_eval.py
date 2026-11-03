"""Standalone Evaluation Harness Benchmark Runner.

Run with: python tests/harness/run_eval.py
"""

import sys
import os
import json
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.agent.langchain_agent import LangChainAgent
from app.db.database import db_manager

def run_benchmark():
    db_manager.init_database(force_reload=False)
    agent = LangChainAgent(provider="mock")

    dataset_path = Path(__file__).parent / "golden_dataset.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    print("=" * 80)
    print("EMPÓRIO DA MÚSICA - AI AGENT EVALUATION HARNESS BENCHMARK")
    print("=" * 80)

    total = len(cases)
    passed = 0
    guardrail_correct = 0
    guardrail_total = 0
    tool_correct = 0
    tool_total = 0

    start_time = time.time()

    for idx, case in enumerate(cases, 1):
        case_id = case["id"]
        category = case["category"]
        query = case["user_query"]
        expected_tool = case.get("expected_tool")
        expected_guardrail = case.get("expected_guardrail", False)
        required_words = case.get("required_in_response", [])
        forbidden_words = case.get("forbidden_in_response", [])

        t0 = time.time()
        res = agent.process_message(query, session_id=f"eval_{case_id}", force_mock=True)
        elapsed = (time.time() - t0) * 1000

        resp_lower = res["response"].lower()
        guard_ok = (expected_guardrail == res["guardrail_triggered"])
        if expected_guardrail:
            guardrail_total += 1
            if guard_ok:
                guardrail_correct += 1

        tool_ok = True
        if not expected_guardrail and expected_tool:
            tool_total += 1
            tool_ok = (expected_tool in res["tools_used"])
            if tool_ok:
                tool_correct += 1

        req_ok = all(w.lower() in resp_lower for w in required_words)
        forb_ok = not any(w.lower() in resp_lower for w in forbidden_words)

        case_passed = guard_ok and tool_ok and req_ok and forb_ok
        if case_passed:
            passed += 1
            status_tag = "[PASS]"
        else:
            status_tag = "[FAIL]"

        print(f"{status_tag} Case {idx:02d} [{category}]: {query[:45]:<45} ({elapsed:.1f}ms)")
        if not case_passed:
            print(f"       Errors: guard_ok={guard_ok}, tool_ok={tool_ok}, req_ok={req_ok}, forb_ok={forb_ok}")

    total_time = time.time() - start_time
    acc = (passed / total) * 100
    guard_acc = (guardrail_correct / max(1, guardrail_total)) * 100
    tool_acc = (tool_correct / max(1, tool_total)) * 100

    print("-" * 80)
    print("BENCHMARK METRICS SUMMARY:")
    print(f"Total Test Cases:         {total}")
    print(f"Passed Cases:             {passed} / {total} ({acc:.1f}%)")
    print(f"Guardrail Precision:      {guardrail_correct} / {guardrail_total} ({guard_acc:.1f}%)")
    print(f"Tool Routing Accuracy:    {tool_correct} / {tool_total} ({tool_acc:.1f}%)")
    print(f"Total Evaluation Time:    {total_time:.2f}s")
    print("=" * 80)

if __name__ == "__main__":
    run_benchmark()

