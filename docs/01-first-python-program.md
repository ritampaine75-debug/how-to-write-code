# Writing Your First Python Program, Step by Step

*Part 1 of the [How to Write Code](../README.md) series.*

This page shows the shortest possible path from an empty computer to a running program.

## What you need

- Python 3.8 or newer installed (check with `python --version`)
- A text editor (VS Code recommended) or any browser-based Python editor
- About 10 minutes

## Step 1 — Create the file

Create a folder called `learn-code`, then inside it create a file named `hello.py`.

The `.py` ending tells the computer the file contains Python code.

## Step 2 — Type one line of code

```python
print("Hello, World!")
```

`print()` is a built-in function that sends whatever is inside the brackets to the screen. Text must be wrapped in quotes — that is called a **string**.

## Step 3 — Run the file

Open a terminal in the same folder and run:

```bash
python hello.py
```

You should see:

```text
Hello, World!
```

If you instead see `python: command not found`, try `python3 hello.py` (common on macOS and Linux).

## Step 4 — Make it interactive

Now accept input from the user:

```python
name = input("What is your name? ")
print(f"Hello, {name}! Welcome to programming.")
```

Run it:

```bash
python hello.py
```

```text
What is your name? Rita
Hello, Rita! Welcome to programming.
```

The `f"..."` prefix creates an **f-string**, which lets you drop variables directly into text with `{}`.

## Step 5 — Save it to Git

```bash
git init
git add hello.py
git commit -m "Add first Python program"
```

Now your work has a saved history you can return to.

## Common first-run errors

| Message | Cause | Fix |
|---|---|---|
| `SyntaxError: invalid syntax` | Missing closing quote or bracket | Count your quotes |
| `command not found: python` | Python not on PATH | Use `python3` instead |
| `FileNotFoundError` | Wrong folder | `cd` into the folder that holds the file |

## Next step

Continue to [Variables, data types and operators](02-variables-and-data-types.md).
