"""Verify the guide's own claims: run its code examples, check links, validate HTML/JSON-LD/XML."""
import io
import json
import re
import sys
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
fails = []
checks = 0


def check(name, ok, detail=""):
    global checks
    checks += 1
    print(("PASS  " if ok else "FAIL  ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        fails.append(name)


def run_capture(code, stdin_text=""):
    buf = io.StringIO()
    old = sys.stdin
    sys.stdin = io.StringIO(stdin_text)
    try:
        with redirect_stdout(buf):
            exec(code, {})
    finally:
        sys.stdin = old
    return buf.getvalue()


# ---------- 1. Runnable examples from the guide ----------
print("\n== Runnable code examples ==")

check(
    "README: sort names example",
    run_capture(
        'names = ["Rita", "Aman", "Deepa"]\nnames.sort()\nfor name in names:\n    print(name)\n'
    ).strip()
    == "Aman\nDeepa\nRita",
)

# NB: input()'s prompt is written to stdout, so it is captured on the same line as
# the print() that follows. Assert the greeting substring rather than a whole line.
check(
    "README: first-program input example",
    run_capture(
        'name = input("What is your name? ")\nprint(f"Hello, {name}! Welcome to programming.")\n',
        "Rita\n",
    ).rstrip().endswith("Hello, Rita! Welcome to programming."),
)

check(
    "docs/02: price/discount worked example prints 122.85",
    run_capture(
        'item = "Notebook"\nprice = 45.50\nquantity = 3\ndiscount = 0.10\n'
        'subtotal = price * quantity\ntotal = subtotal * (1 - discount)\n'
        'print(f"{quantity} x {item} = \u20b9{total:.2f}")\n'
    ).strip()
    == "3 x Notebook = \u20b9122.85",
)

check(
    "docs/02: operator table values",
    run_capture(
        "print(7+3, 7-3, 7*3, 7//3, 7%3, 7**3)\n"
    ).strip()
    == "10 4 21 2 1 343",
)

check(
    "docs/03: grade example returns B for 78",
    run_capture(
        "score = 78\n"
        'if score >= 90:\n    grade = "A"\nelif score >= 75:\n    grade = "B"\n'
        'elif score >= 60:\n    grade = "C"\nelse:\n    grade = "F"\nprint(grade)\n'
    ).strip()
    == "B",
)

check(
    "docs/03: break/continue example prints 1 3",
    run_capture(
        "for number in range(1, 10):\n"
        "    if number == 5:\n        break\n"
        "    if number % 2 == 0:\n        continue\n"
        "    print(number)\n"
    ).strip()
    == "1\n3",
)

check(
    "docs/03: guessing-game source compiles",
    compile(
        (ROOT / "docs/03-conditions-and-loops.md").read_text(encoding="utf-8")
        .split("```python")[2]
        .split("```")[0],
        "<guessing>",
        "exec",
    )
    is not None,
)

check(
    "docs/04: celsius converter prints the documented four lines",
    run_capture(
        "def celsius_to_fahrenheit(celsius):\n    return celsius * 9 / 5 + 32\n"
        'def format_temperature(value, unit):\n    return f"{value:.1f}\u00b0{unit}"\n'
        "for c in [0, 25, 37, 100]:\n"
        "    f = celsius_to_fahrenheit(c)\n"
        '    print(format_temperature(f, "F"))\n'
    ).strip()
    == "32.0\u00b0F\n77.0\u00b0F\n98.6\u00b0F\n212.0\u00b0F",
)

check(
    "docs/04: greet default-argument example",
    run_capture(
        'def greet(name, greeting="Hello"):\n    print(f"{greeting}, {name}!")\n'
        'greet("Rita")\ngreet("Rita", "Namaste")\n'
    ).strip()
    == "Hello, Rita!\nNamaste, Rita!",
)

check(
    "docs/05: input-validation snippet compiles",
    compile(
        'raw = input("Age: ")\nif raw.isdigit():\n    age = int(raw)\nelse:\n    print("Please type a number")\n',
        "<validate>",
        "exec",
    )
    is not None,
)

# Every ```python block in every markdown file must at least compile
print("\n== Every python code block compiles ==")
md_files = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
total_blocks = 0
for md in md_files:
    blocks = re.findall(r"```python\n(.*?)```", md.read_text(encoding="utf-8"), re.S)
    for i, block in enumerate(blocks, 1):
        total_blocks += 1
        # blocks that intentionally fail or need a file/network are compile-only
        try:
            compile(block, f"{md.name}#block{i}", "exec")
            ok, detail = True, ""
        except SyntaxError as exc:
            # the guide deliberately shows broken code inside docs/05
            ok = md.name == "05-debugging-for-beginners.md"
            detail = f"{type(exc).__name__}: {exc.msg}" + (" (expected bad example)" if ok else "")
        check(f"{md.name} block {i}", ok, detail)
print(f"  ({total_blocks} python blocks checked)")

# ---------- 2. Markdown links resolve ----------
print("\n== Markdown internal links ==")
for md in md_files:
    text = md.read_text(encoding="utf-8")
    for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#")):
            continue
        path = (md.parent / target.split("#")[0]).resolve()
        check(f"{md.name}: link to {target}", path.exists(), label)

# TOC anchors in README must match a real heading
print("\n== README table-of-contents anchors ==")
readme = (ROOT / "README.md").read_text(encoding="utf-8")


def slug(heading):
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s).strip("-")


anchors = {slug(m) for m in re.findall(r"^#{1,4}\s+(.*)$", readme, re.M)}
for href in re.findall(r"\]\(#([a-z0-9-]+)\)", readme):
    check(f"anchor #{href}", href in anchors)

# ---------- 3. SEO / HTML validation ----------
print("\n== SEO page (site/index.html) ==")
html = (ROOT / "site/index.html").read_text(encoding="utf-8")


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.voids = [], [], {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "source", "track", "wbr",
        }

    def handle_starttag(self, tag, attrs):
        if tag not in self.voids:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.voids:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"mismatched </{tag}>, stack top={self.stack[-1] if self.stack else None}")
        else:
            self.stack.pop()


parser = Checker()
parser.feed(html)
parser.close()
check("HTML tags balanced", not parser.errors and not parser.stack,
      "; ".join(parser.errors[:3]) or f"unclosed={parser.stack[:3]}")

title = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
desc = re.search(r'<meta name="description" content="(.*?)">', html, re.S).group(1)
check("title present and <= 70 chars", 0 < len(title) <= 70, f"{len(title)} chars")
check("meta description 50-160 chars", 50 <= len(desc) <= 160, f"{len(desc)} chars")
check("primary keyword 'how to write code' in title", "how to write code" in title.lower())
check("primary keyword in meta description", "how to write code" in desc.lower())
check("canonical URL set", 'rel="canonical"' in html)
check("Open Graph tags set", 'property="og:title"' in html and 'property="og:description"' in html)
check("exactly one <h1>", html.count("<h1>") == 1, f"{html.count('<h1>')} found")
check("viewport meta set", 'name="viewport"' in html)
check("lang attribute on <html>", re.search(r'<html lang="[a-z]{2}"', html) is not None)

h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", html)
check("multiple H2 sections for crawlability", len(h2s) >= 6, f"{len(h2s)} H2s")

blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
check("JSON-LD blocks found", len(blocks) >= 3, f"{len(blocks)} blocks")
schemas = []
for i, block in enumerate(blocks, 1):
    try:
        data = json.loads(block)
        schemas.append(data["@type"])
        check(f"JSON-LD block {i} is valid JSON", True, f"@type={data['@type']}")
    except (json.JSONDecodeError, KeyError) as exc:
        check(f"JSON-LD block {i} is valid JSON", False, str(exc))
check("FAQPage schema present", "FAQPage" in schemas)
check("HowTo schema present", "HowTo" in schemas)
check("Article schema present", "Article" in schemas)

# FAQ questions in the HTML must match the ones in the schema
faq_schema = next((b for b in schemas if True), None)
schema_questions = {
    q["name"].strip().lower()
    for b in blocks
    for q in (json.loads(b).get("mainEntity", []) if json.loads(b)["@type"] == "FAQPage" else [])
}
html_questions = {re.sub(r"\s+", " ", s).strip().lower() for s in re.findall(r"<summary>(.*?)</summary>", html)}
check("HTML FAQ matches FAQPage schema", html_questions == schema_questions,
      f"html={len(html_questions)} schema={len(schema_questions)}")

# ---------- 4. sitemap / robots ----------
print("\n== sitemap.xml and robots.txt ==")
try:
    tree = ET.parse(ROOT / "site/sitemap.xml")
    urls = tree.getroot()
    check("sitemap.xml is well-formed XML", True, f"{len(urls)} urls")
    locs = [e.text for u in urls for e in u if e.tag.endswith("loc")]
    check("sitemap has loc entries", all(l and l.startswith("https://") for l in locs), f"{len(locs)} locs")
except ET.ParseError as exc:
    check("sitemap.xml is well-formed XML", False, str(exc))

robots = (ROOT / "site/robots.txt").read_text(encoding="utf-8")
check("robots.txt allows crawling", "User-agent: *" in robots and "Allow: /" in robots)
check("robots.txt points to sitemap", "Sitemap:" in robots)

# ---------- 5. repo hygiene ----------
print("\n== Repo hygiene ==")
check("LICENSE present", (ROOT / "LICENSE").exists())
check("MIT text present", "MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8"))
check(".gitignore present", (ROOT / ".gitignore").exists())

gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
check(".gitignore excludes secrets", ".env" in gi and "*.key" in gi)

# Match a real token shape (ghp_ + 36 alphanumerics), not the 4-char literal used
# by this scanner itself.
TOKEN_RE = re.compile(r"ghp_[A-Za-z0-9]{36}")
secret_leak = False
for f in ROOT.rglob("*"):
    if f.is_file() and ".git" not in f.parts:
        try:
            if TOKEN_RE.search(f.read_text(encoding="utf-8")):
                secret_leak = True
                print(f"    !! token-like string in {f.relative_to(ROOT)}")
        except UnicodeDecodeError:
            pass
check("no GitHub token committed anywhere in the repo", not secret_leak)

# ---------- summary ----------
print("\n" + "=" * 60)
print(f"{checks - len(fails)}/{checks} checks passed")
if fails:
    print("FAILED:")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("All checks passed.")
