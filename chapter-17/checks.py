def draft_checks(order: str, draft: dict, calls: list) -> list[str]:
    """Rules a program can check exactly, now on named fields and tool calls.
    `order` is the order number the email gives, or "" when it gives none."""
    problems = []
    if len(draft["reply"].split()) > 120:
        problems.append("over 120 words")
    if "The support team" not in draft["reply"]:
        problems.append("missing sign-off")
    if draft["order_number"] != order:
        problems.append(f"order_number is {draft['order_number']!r}")
    if order and not any(name == "lookup_order" and args.get("order_number") == order
                         for name, args, _ in calls):
        problems.append(f"order {order} not looked up")
    if draft["category"] == "refund_or_return" and not draft["needs_person"]:
        problems.append("refund request not handed to a person")
    return problems
