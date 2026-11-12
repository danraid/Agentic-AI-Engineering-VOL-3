# Additional illustrative Python fragments

## Fragment 1

```python
from hashlib import sha256
from pathlib import Path

chapter = Path("chapter.md").read_bytes()
if chapter.startswith(b"\xef\xbb\xbf") or b"\r" in chapter:
    raise SystemExit("Expected UTF-8 without BOM and with LF line endings")
chapter.decode("utf-8")

begin = b"<!-- LAB:BEGIN -->\n```python\n"
end = b"```\n<!-- LAB:END -->"
if chapter.count(begin) != 1 or chapter.count(end) != 1:
    raise SystemExit("Expected exactly one matching laboratory block")

start = chapter.index(begin) + len(begin)
stop = chapter.index(end, start)
source = chapter[start:stop]
if not source.endswith(b"\n"):
    raise SystemExit("Laboratory source must end with LF")

Path("governance_lab.py").write_bytes(source)
print("chapter SHA-256:", sha256(chapter).hexdigest())
print("laboratory-source SHA-256:", sha256(source).hexdigest())
```
