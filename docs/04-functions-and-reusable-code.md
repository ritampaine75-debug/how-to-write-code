# Functions: Writing Reusable Code

*Part 4 of the [How to Write Code](../README.md) series.*

A **function** is a named block of code you can run whenever you want. Functions are how you stop repeating yourself.

## Defining and calling a function

```python
def greet():
    print("Hello!")

greet()   # Hello!
greet()   # Hello!  — reusable
```

- `def` starts the definition
- `greet` is the function name
- `()` holds the inputs, if any
- The indented block is the body
- Calling means writing the name with `()`

## Passing data in: parameters

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Rita")    # Hello, Rita!
greet("Aman")    # Hello, Aman!
```

`name` is a **parameter** (the placeholder). `"Rita"` is an **argument** (the real value).

## Default values

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Rita")                 # Hello, Rita!
greet("Rita", "Namaste")      # Namaste, Rita!
```

Parameters with defaults must come after parameters without them.

## Getting data out: `return`

`print()` shows a value to a human. `return` hands a value back to your code so it can be reused.

```python
def area(length, width):
    return length * width

room = area(4, 5)      # room is now 20
print(room * 2)        # 40
```

A function without `return` gives back `None`.

## Keeping functions small

A good function does **one** thing. Compare:

```python
# Hard to reuse
def process():
    data = input("Numbers: ").split(",")
    numbers = [int(n) for n in data]
    total = sum(numbers)
    print(f"Total is {total}")

# Reusable pieces
def read_numbers():
    return [int(n) for n in input("Numbers: ").split(",")]

def report_total(numbers):
    print(f"Total is {sum(numbers)}")

report_total(read_numbers())
```

The second version lets you reuse `read_numbers()` somewhere else without the printing.

## Worked example: a small toolbox

```python
def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

def format_temperature(value, unit):
    return f"{value:.1f}°{unit}"

for c in [0, 25, 37, 100]:
    f = celsius_to_fahrenheit(c)
    print(format_temperature(f, "F"))
```

Output:

```text
32.0°F
77.0°F
98.6°F
212.0°F
```

## Scope: where variables exist

A variable created inside a function cannot be seen outside it.

```python
def demo():
    message = "inside"

demo()
print(message)   # NameError: name 'message' is not defined
```

Return the value if you need it outside.

## Next step

Continue to [Debugging for beginners](05-debugging-for-beginners.md).
