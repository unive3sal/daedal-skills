#!/usr/bin/env python3
"""Validate crate-research eval data without third-party dependencies."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():
    suite = json.loads((ROOT / "evals.json").read_text())
    triggers = json.loads((ROOT / "trigger-evals.json").read_text())
    assert suite["skill_name"] == "crate-research"
    ids = [case["id"] for case in suite["evals"]]
    assert len(ids) == len(set(ids)), "Duplicate behavior case IDs"
    assert len(suite["evals"]) >= 10, "Missing behavior coverage"
    for case in suite["evals"]:
        assert case["prompt"] and case["expected_output"]
        assert case["expectations"], f"No assertions for case {case['id']}"
        for relative in case["files"]:
            assert (ROOT.parent / relative).is_file(), relative
    assert len(triggers) == 20, "Expected 20 trigger examples"
    assert sum(item["should_trigger"] for item in triggers) == 10
    for item in triggers:
        assert isinstance(item["should_trigger"], bool)
        assert item["query"]
    for path in ROOT.rglob("*"):
        if path.suffix in {".json", ".md"}:
            assert not re.search(r"[㐀-鿿]", path.read_text()), (
                f"Non-English CJK prose in {path}"
            )
    skill = (ROOT.parent / "SKILL.md").read_text()
    description = next(line[13:] for line in skill.splitlines()
                       if line.startswith("description: "))
    assert len(description) <= 1024, "Description exceeds common skill limit"
    assert len(skill.splitlines()) < 500
    print(f"Validated {len(ids)} behavior cases and {len(triggers)} trigger cases.")
    print("Fixture paths, assertions, CJK-language check, and metadata limits passed.")
    print("This is structural validation, not agent activation or behavior evaluation.")


if __name__ == "__main__":
    main()
