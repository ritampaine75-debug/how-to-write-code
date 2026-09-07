# Variables, Data Types and Operators Explained

*Part 2 of the [How to Write Code](../README.md) series.*

A **variable** is a labelled box that holds a value. You create one with a single `=` sign.

```python
name = "Rita"      # text
age = 25           # whole number
height = 1.68      # decimal number
is_student = True  # true/false
```

## The four basic data types

| Type | Python name | Example | Used for |
|---|---|---|---|
| Text | `str` | `"Hello"` | Names, messages, file contents |
| Whole number | `int` | `42` | Counts, ages, indexes |
| Decimal | `float` | `3.14` | Money, measurements |
| True/False | `bool` | `True` | Conditions and flags |

Check any value's type:

```python
print(type("Hello"))   # <class 'str'>
print(type(42))        # <class 'int'>
```

## Converting between types

```python
age_text = input("Your age: ")   # input() always returns a string
age = int(age_text)              # convert to a number
print(age + 1)
```

Skipping the conversion is the cause of the classic `TypeError: can only concatenate str (not "int") to str`.

## Operators

### Arithmetic

```python
print(7 + 3)    # 10  addition
print(7 - 3)    # 4   subtraction
print(7 * 3)    # 21  multiplication
print(7 / 3)    # 2.333...  division
print(7 // 3)   # 2   whole-number division
print(7 % 3)    # 1   remainder
print(7 ** 3)   # 343 power
```

### Comparison — always produce `True` or `False`

```python
print(5 > 3)     # True
print(5 == 5)    # True   (two equals means "is equal")
print(5 != 5)    # False  (not equal)
```

### Logic

```python
has_ticket = True
is_early = False
print(has_ticket and is_early)  # False
print(has_ticket or is_early)   # True
print(not has_ticket)           # False
```

## Naming rules

- Start with a letter or underscore, never a digit: `age2` is valid, `2age` is not.
- No spaces — use underscores: `total_price`.
- Case matters: `Score` and `score` are different variables.
- Avoid Python's reserved words such as `if`, `for`, `class`, `print`.

## Worked example

```python
item = "Notebook"
price = 45.50
quantity = 3
discount = 0.10

subtotal = price * quantity
total = subtotal * (1 - discount)

print(f"{quantity} x {item} = ₹{total:.2f}")
# 3 x Notebook = ₹122.85
```

`{total:.2f}` rounds the number to two decimal places.

## Next step

Continue to [Conditions and loops](03-conditions-and-loops.md).
