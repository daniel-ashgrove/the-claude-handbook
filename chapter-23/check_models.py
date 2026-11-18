"""Warn before a model your code uses is retired."""
import sys

import anthropic

MODELS = ["claude-sonnet-5-5", "claude-opus-5-5"]  # the drafter and the grader


def check(client: anthropic.Anthropic, wanted: list[str]) -> list[str]:
    """One line for each model in `wanted` that needs attention."""
    known = {m.id: m for m in client.models.list(
        lifecycle=["active", "deprecated", "retired"])}
    problems = []
    for model_id in wanted:
        info = known.get(model_id)
        if info is None:
            problems.append(f"{model_id}: not available to this organization")
        elif info.lifecycle != "active":
            when = info.retires_at.date() if info.retires_at else "not set"
            problems.append(f"{model_id}: {info.lifecycle}, retirement {when}")
    return problems


if __name__ == "__main__":
    problems = check(anthropic.Anthropic(), MODELS)
    print("\n".join(problems) or "All models active.")
    sys.exit(1 if problems else 0)
