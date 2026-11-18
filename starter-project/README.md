# Starter project: shop-tools

A small Python project for practising with Claude Code. Use it for the practices in Chapters 11, 12 and 14 of *The Claude Handbook* if you don't have a project of your own, or would rather practise on one you can't break.

It belongs to an invented online homeware shop, the same one the book's later chapters use. It works out what a customer pays (the basket, any discount code, then delivery) and when an order should arrive. It has tests, and one bug a customer has reported (below). It needs nothing beyond Python itself.

## What you need

- **Python 3.10 or later.** Check with `python3 --version` on macOS, Linux or WSL, or `py --version` on Windows. If you don't have it, install it from python.org.
- **git.** Check with `git --version`. If you don't have it, install it from git-scm.com.
- **Claude Code**, installed as Chapter 11 shows.

## Make your own copy

The project needs to be its own git repository, so copy the folder out of this one and start a fresh history.

On macOS, Linux or WSL:

```bash
git clone https://github.com/daniel-ashgrove/the-claude-handbook.git
cp -r the-claude-handbook/starter-project starter-project
cd starter-project
git init
git add .
git commit -m "Starting point"
```

On Windows, in PowerShell:

```powershell
git clone https://github.com/daniel-ashgrove/the-claude-handbook.git
Copy-Item -Recurse the-claude-handbook\starter-project starter-project
cd starter-project
git init
git add .
git commit -m "Starting point"
```

If git asks who you are, set your name and email once with `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`, then run the commit again.

## Run the tests

From inside `starter-project`:

- macOS, Linux or WSL: `python3 -m unittest`
- Windows: `py -m unittest`

You should see `Ran 10 tests` and `OK`. The tests pass even though the project has a bug, because no test covers it yet.

## What's inside

| File | What it does |
|---|---|
| `shop_tools/orders.py` | Adds up a basket, applies a discount code, adds delivery |
| `shop_tools/delivery.py` | The delivery charge, and the arrival date counted in working days |
| `tests/` | The tests, written with Python's built-in `unittest` |
| `tests/test_settings.env` | Settings for a test payment service. The values are made up, but treat the file as if they were real: Chapter 11's practice has you add a deny rule for it |

There is no `CLAUDE.md`. Chapter 11's practice has you create one with `/init`.

## The reported bug (for Chapter 12)

A customer writes: "My basket came to exactly 50.00 and I was charged 4.95 for delivery. Your site says delivery is free from 50.00."

The shop's rule is free delivery for a basket of 50.00 or more, after any discount. Describe this to Claude the way Section 12.2 shows: the symptom, where you think the problem is, and what fixed looks like, with a test that reproduces the bug before the fix. When it is fixed, the new test passes and so do the other ten.

## A change to try (for Chapter 14)

Add an express delivery option: 9.50, arriving in one working day, and never free. Work on a branch, as Chapter 14 shows.

To try Chapter 14's pull request step, your copy needs to be on GitHub. With GitHub's `gh` tool installed and signed in (`gh auth login`), run this once from inside `starter-project`:

```bash
gh repo create starter-project --private --source=. --push
```

That creates a private repository under your own account and pushes your copy to it. Delete it on GitHub when you have finished.
