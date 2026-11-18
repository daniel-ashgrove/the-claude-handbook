import sys

from checks import draft_checks
from draft_reply import Effort, draft
from grader import graded_check
from shop_data import TICKETS

RUNS = 3  # replies vary from run to run, so test each case more than once
# The order number each ticket's email gives, or "" when it gives none.
EXPECTED_ORDER = {"812": "4471", "813": "5120", "814": "3388",
                  "815": "", "816": "", "817": "9999"}


def main(effort: Effort):
    passed = total = 0
    for ticket_id, ticket in TICKETS.items():
        for run in range(1, RUNS + 1):
            result, calls = draft(ticket_id, effort=effort)
            problems = (draft_checks(EXPECTED_ORDER[ticket_id], result, calls)
                        + graded_check(ticket["body"], result["reply"]))
            total += 1
            passed += not problems
            print(f"{ticket_id} {ticket['subject']:16} run {run}  "
                  f"{'PASS' if not problems else 'FAIL'}  " + "; ".join(problems))
    print(f"\nEffort {effort}: {passed}/{total} drafts passed every check")


if __name__ == "__main__":
    level = sys.argv[1] if len(sys.argv) > 1 else "high"
    if level not in ("low", "medium", "high", "xhigh", "max"):
        sys.exit("Effort must be low, medium, high, xhigh or max")
    main(level)
