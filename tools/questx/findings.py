"""Quest-line findings for the explorer: item tasks already covered by upstream rewards, quests on one spot, main quests behind side quests."""
from collections import Counter
from dataclasses import dataclass

from tools.questgen.model import Chapter


@dataclass(frozen=True)
class Finding:
    chapter: str
    slug: str
    kind: str  # covered, partly-covered, same-position, main-needs-side
    message: str

    def line(self) -> str:
        return f"{self.chapter}:{self.slug}: {self.message}"


def _ancestors(key, quests) -> set:
    seen, todo = set(), list(quests[key].dep_keys())
    while todo:
        dep = todo.pop()
        if dep not in seen and dep in quests:
            seen.add(dep)
            todo.extend(quests[dep].dep_keys())
    return seen


def find(chapters: list[Chapter]) -> list[Finding]:
    quests = {(c.slug, q.slug): q for c in chapters for q in c.quests}
    group_of = {c.slug: c.group for c in chapters}
    findings = []
    for c in chapters:
        for q in c.quests:
            given, givers = Counter(), {}
            for key in sorted(_ancestors((c.slug, q.slug), quests)):
                for r in quests[key].rewards:
                    if r.get("type") == "item":
                        given[r["item"]] += r.get("count", 1)
                        givers.setdefault(r["item"], []).append(":".join(key))
            for t in q.tasks:
                if t.get("type") != "item" or not given[t["item"]]:
                    continue
                need, have = t.get("count", 1), given[t["item"]]
                source = ", ".join(givers[t["item"]])
                if have >= need:
                    findings.append(Finding(c.slug, q.slug, "covered",
                                            f"task {need} {t['item']} is already covered by rewards of {source}"))
                else:
                    findings.append(Finding(c.slug, q.slug, "partly-covered",
                                            f"task {need} {t['item']}: {have} come from rewards of {source}"))
            if c.group == "main":
                for dep in q.dep_keys():
                    if group_of.get(dep[0]) == "side":
                        findings.append(Finding(c.slug, q.slug, "main-needs-side",
                                                f"main quest depends on side quest {':'.join(dep)}"))
        at = {}
        for q in c.quests:
            other = at.setdefault((q.x, q.y), q.slug)
            if other != q.slug:
                findings.append(Finding(c.slug, q.slug, "same-position",
                                        f"same position ({q.x:g}, {q.y:g}) as {c.slug}:{other}"))
    return findings
