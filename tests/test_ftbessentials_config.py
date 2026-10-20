"""The shipped FTB Essentials config keeps /rtp off (docs/gates.md); a mod update can bring the default back."""
import re
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "config/ftbessentials.json5"


def block(text: str, name: str) -> str:
    """The body of the first `name: { ... }` object in JSON5 text without comments."""
    start = re.search(rf"\b{name}\s*:\s*\{{", text).end()
    depth = 1
    for i in range(start, len(text)):
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        if depth == 0:
            return text[start:i]
    raise ValueError(f"unclosed block {name}")


def top_level(body: str) -> str:
    """The body with nested objects removed, so only its own keys remain."""
    while (stripped := re.sub(r"\{[^{}]*\}", "", body)) != body:
        body = stripped
    return body


def rtp_enabled(text: str) -> bool:
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    rtp = top_level(block(block(text, "teleportation"), "rtp"))
    return re.search(r"\benabled\s*:\s*(true|false)", rtp).group(1) == "true"


def test_rtp_is_off():
    assert not rtp_enabled(CONFIG.read_text(encoding="utf-8"))


def test_rtp_on_is_detected():
    text = CONFIG.read_text(encoding="utf-8")
    on = re.sub(r"(\brtp\s*:\s*\{.*?\benabled\s*:\s*)false", r"\1true", text, count=1, flags=re.S)
    assert rtp_enabled(on)
