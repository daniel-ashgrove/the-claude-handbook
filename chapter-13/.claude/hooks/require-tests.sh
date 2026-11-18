#!/bin/bash
# Don't let Claude finish while the tests fail.
INPUT=$(cat)
cd "$CLAUDE_PROJECT_DIR" || exit 0

# Already sent back once by this hook? Let Claude stop.
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0
fi

# Nothing changed since the last commit? Nothing to check.
if [ -z "$(git status --porcelain)" ]; then
  exit 0
fi

if ! OUTPUT=$(npm test 2>&1); then
  echo "The tests are failing. Fix them before you finish:" >&2
  echo "$OUTPUT" | tail -n 30 >&2
  exit 2
fi

exit 0
