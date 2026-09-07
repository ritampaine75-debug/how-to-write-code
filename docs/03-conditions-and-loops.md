# Conditions and Loops: Controlling Program Flow

*Part 3 of the [How to Write Code](../README.md) series.*

By default code runs top to bottom. **Conditions** let it choose a path; **loops** let it repeat.

## Conditions with `if`, `elif`, `else`

```python
score = 78

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(grade)   # B
```

Three syntax rules that catch out every beginner:

1. The condition line ends with a colon `:`
2. The indented block below it is what runs
3. Python checks conditions top to bottom and stops at the first match

## `for` loops — repeat over a collection

```python
for fruit in ["mango", "banana", "guava"]:
    print(fruit)
```

Use `range()` to repeat a fixed number of times:

```python
for i in range(1, 6):      # 1 up to but not including 6
    print(i)
# 1 2 3 4 5
```

## `while` loops — repeat until a condition changes

```python
count = 0
while count < 3:
    print(count)
    count += 1     # without this line the loop never ends
```

A `while` loop whose condition can never become `False` is an **infinite loop**. Press `Ctrl + C` in the terminal to stop it.

## `break` and `continue`

```python
for number in range(1, 10):
    if number == 5:
        break          # stop the loop entirely
    if number % 2 == 0:
        continue       # skip the rest and go to the next number
    print(number)
# 1 3
```

## Worked example: number guessing game

```python
import random

secret = random.randint(1, 10)
attempts = 0

while True:
    guess = int(input("Guess a number 1-10: "))
    attempts += 1

    if guess < secret:
        print("Too low")
    elif guess > secret:
        print("Too high")
    else:
        print(f"Correct in {attempts} tries!")
        break
```

This single program uses variables, conditions, a loop, `break`, and type conversion — the core of writing code.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Forgetting the colon | `SyntaxError` | End the `if`/`for`/`while` line with `:` |
| Inconsistent indentation | `IndentationError` | Use exactly 4 spaces |
| Using `=` in a condition | `SyntaxError` | Comparisons need `==` |
| Never changing a `while` variable | Program hangs | Update the variable inside the loop |

## Next step

Continue to [Functions and reusable code](04-functions-and-reusable-code.md).
