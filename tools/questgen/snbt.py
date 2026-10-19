"""Deterministic SNBT writer in the layout FTB Quests uses: tabs, one entry per line, sorted keys."""
import re
from dataclasses import dataclass

_BARE_KEY = re.compile(r"^[A-Za-z0-9_.+-]+$")


@dataclass(frozen=True)
class Double:
    value: float


@dataclass(frozen=True)
class Long:
    value: int


@dataclass(frozen=True)
class Byte:
    value: int


def _number(value: float) -> str:
    text = repr(float(value))
    return text if "e" in text or "." in text else text + ".0"


def quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def _key(key: str) -> str:
    return key if _BARE_KEY.match(key) else quote(key)


def _scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Double):
        return _number(value.value) + "d"
    if isinstance(value, Long):
        return f"{value.value}L"
    if isinstance(value, Byte):
        return f"{value.value}b"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return _number(value) + "d"
    if isinstance(value, str):
        return quote(value)
    raise TypeError(f"cannot write {type(value).__name__} as SNBT")


def dumps(value, indent: int = 0) -> str:
    pad = "\t" * indent
    inner = "\t" * (indent + 1)
    if isinstance(value, dict):
        if not value:
            return "{ }"
        lines = [f"{inner}{_key(k)}: {dumps(value[k], indent + 1)}" for k in sorted(value)]
        return "{\n" + "\n".join(lines) + f"\n{pad}}}"
    if isinstance(value, (list, tuple)):
        if not value:
            return "[ ]"
        lines = [f"{inner}{dumps(v, indent + 1)}" for v in value]
        return "[\n" + "\n".join(lines) + f"\n{pad}]"
    return _scalar(value)


def dump_file(value) -> str:
    return dumps(value) + "\n"
