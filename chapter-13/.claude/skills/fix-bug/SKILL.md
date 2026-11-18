---
description: Fix a reported bug, test first. Use when I describe a bug to fix.
argument-hint: [what goes wrong]
disable-model-invocation: true
---

Fix this bug: $ARGUMENTS

1. Find where the behavior comes from. Tell me which files are involved
   before you edit anything.
2. Write a test that fails because of the bug. Run it and show me the failure.
3. Make the smallest change that fixes it.
4. Run that test and then the full test suite. Show me the output of both.
5. Summarize what changed and why in no more than three sentences.
