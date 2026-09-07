# Debugging for Beginners: Fixing Your First 20 Errors

*Part 5 of the [How to Write Code](../README.md) series.*

Every error message follows the same shape. Once you can read one, you can read all of them.

## Anatomy of a traceback

```text
Traceback (most recent call last):
  File "shop.py", line 12, in <module>
    total = price * quantity
NameError: name 'quantity' is not defined
```

| Part | Tells you |
|---|---|
| `File "shop.py", line 12` | Where to look |
| `total = price * quantity` | The line that failed |
| `NameError` | The category of problem |
| `name 'quantity' is not defined` | The specific cause |

Read the **last line first**. It is the summary.

## The 20 errors beginners hit most often

### 1. `SyntaxError: expected ':'`

```python
if age > 18        # missing colon
```

Fix: `if age > 18:`

### 2. `SyntaxError: unterminated string literal`

```python
print("Hello)      # missing closing quote
```

Fix: `print("Hello")`

### 3. `IndentationError: unexpected indent`

Cause: a line is indented when it should not be, or two indentation styles are mixed.

Fix: select the block and re-indent with 4 spaces.

### 4. `IndentationError: expected an indented block`

```python
def greet():
print("hi")        # body must be indented
```

### 5. `NameError: name 'x' is not defined`

Causes: a typo, the variable was created inside a function, or you used it before defining it.

### 6. `TypeError: can only concatenate str (not "int") to str`

```python
age = input("Age: ")     # this is text, e.g. "25"
print("Next year: " + age + 1)   # fails
```

Fix: `age = int(input("Age: "))`

### 7. `TypeError: unsupported operand type(s) for *: 'str' and 'str'`

Cause: multiplying two strings. Convert one to a number first.

### 8. `ValueError: invalid literal for int() with base 10: 'abc'`

Cause: `int("abc")`. The user typed something that is not a number.

Fix: validate before converting.

```python
raw = input("Age: ")
if raw.isdigit():
    age = int(raw)
else:
    print("Please type a number")
```

### 9. `IndexError: list index out of range`

```python
fruits = ["mango", "banana"]
print(fruits[2])    # only indexes 0 and 1 exist
```

Fix: remember the first item is index `0`, and the last valid index is `len(fruits) - 1`.

### 10. `KeyError: 'email'`

```python
user = {"name": "Rita"}
print(user["email"])   # that key does not exist
```

Fix: use `user.get("email", "not provided")`.

### 11. `ZeroDivisionError`

Fix: check the divisor.

```python
if count != 0:
    average = total / count
```

### 12. `AttributeError: 'str' object has no attribute 'append'`

Cause: calling a method the type does not have. Strings are not lists — use `my_list.append(x)`.

### 13. `ModuleNotFoundError: No module named 'requests'`

Fix: `pip install requests`. If you use a virtual environment, make sure it is activated first.

### 14. `FileNotFoundError`

Cause: wrong working directory. Fix: print the path to confirm.

```python
import os
print(os.getcwd())
```

### 15. `TypeError: 'NoneType' object is not subscriptable`

Cause: a function that has no `return` gives `None`, and you indexed the result.

### 16. Infinite loop — the program never stops

Cause: the `while` condition never becomes `False`. Stop it with `Ctrl + C`, then make sure the variable changes inside the loop.

### 17. Code runs but prints nothing

Cause: the function was defined but never called. Add `my_function()`.

### 18. Code prints the function object, not the result

```python
print(greet)     # <function greet at 0x7f...>
print(greet())   # the actual output — note the ()
```

### 19. `=` used instead of `==`

```python
if score = 90:   # SyntaxError — assignment, not comparison
```

### 20. Nothing is wrong, but the old file ran

Cause: you edited one file and ran another, or your editor did not save. Save, then confirm the filename in your `python filename.py` command.

## A debugging routine

1. **Read the last line** of the error.
2. **Search your file** for the word in quotes.
3. **Print the suspects**: `print(repr(value))` shows type and content, including hidden spaces.
4. **Change one thing**, run again.
5. **Rubber duck it**: explain the code line by line out loud. The bug usually reveals itself.
6. **Search the last line** of the error if you are still stuck after 20 minutes.

## Prevention habits

- Run your code every few lines instead of at the end.
- Keep functions short — small code fails in obvious places.
- Write one `assert` or `print` to prove your assumption before building on it.
- Save often with Git so you can compare against a version that worked.

```bash
git add -A && git commit -m "working checkpoint"
```

## Back to the start

Return to the [How to Write Code guide](../README.md).
