"""Writes the explorer page: one index.html with the quest data embedded as JSON, inline CSS and JS, no external URLs."""
import json
from pathlib import Path

from tools.questgen.generate import GROUPS
from tools.questgen.model import Chapter, Quest
from tools.questx.findings import Finding


def quest_icon(q: Quest) -> str:
    return q.icon or next((t["item"] for t in q.tasks if t.get("type") == "item"), "")


def used_items(chapters: list[Chapter]) -> set[str]:
    items = {c.icon for c in chapters if c.icon} | {icon for _, icon in GROUPS.values()}
    for c in chapters:
        for q in c.quests:
            items |= {e["item"] for e in q.tasks + q.rewards if e.get("type") == "item"}
            if quest_icon(q):
                items.add(quest_icon(q))
    return items


def page_data(chapters: list[Chapter], items: dict, findings: list[Finding], built: str) -> dict:
    return {
        "built": built,
        "groups": [{"slug": g, "title": title, "icon": icon} for g, (title, icon) in GROUPS.items()],
        "chapters": [{
            "slug": c.slug, "group": c.group, "title": c.title, "subtitle": c.subtitle, "icon": c.icon,
            "quests": [{
                "slug": q.slug, "title": q.title, "subtitle": q.subtitle, "description": q.description.strip(),
                "x": q.x, "y": q.y, "size": q.size or 1.0, "shape": q.shape or "circle", "optional": q.optional,
                "icon": quest_icon(q), "deps": [list(d) for d in q.dep_keys()], "tasks": q.tasks, "rewards": q.rewards,
            } for q in c.quests],
        } for c in chapters],
        "items": items,
        "findings": [{"chapter": f.chapter, "slug": f.slug, "kind": f.kind, "message": f.message} for f in findings],
    }


def render(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    return TEMPLATE.replace("__DATA__", payload)


def write(out_dir: Path, data: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "index.html"
    path.write_bytes(render(data).encode("utf-8"))
    return path


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quest Explorer</title>
<style>
:root {
  --map: #e8ecef; --dot: #c3ccd3; --panel: #f9fafb; --ink: #1e2a33; --muted: #5d6b76; --line: #d3dbe1;
  --edge: #8794a0; --node: #ffffff; --blue: #1d6db3; --blue-soft: #dbe8f5; --warn: #b26a00; --warn-soft: #fbefd9; --bad: #b3261e;
  --paper: #fffcf3; --paper-ink: #2f2a22; --paper-edge: #e6dcc4; --foot: #eef2f5;
  --slot: #8b8b8b; --slot-dark: #373737; --slot-light: #ffffff;
  --ui: "Segoe UI Variable Text", "Segoe UI", system-ui, sans-serif;
  --letter: "Palatino Linotype", Palatino, "Book Antiqua", "Iowan Old Style", Georgia, serif;
}
@media (prefers-color-scheme: dark) {
  :root {
    --map: #161c22; --dot: #2b3540; --panel: #1c242c; --ink: #e2e8ed; --muted: #95a3ae; --line: #2c3843;
    --edge: #66737f; --node: #222c35; --blue: #6aaeea; --blue-soft: #1d3247; --warn: #e8a33c; --warn-soft: #3a2c14; --bad: #ef7b70;
    --paper: #2a2620; --paper-ink: #efe5d2; --paper-edge: #4a4134; --foot: #182027;
    --slot: #5b5b5b; --slot-dark: #262626; --slot-light: #8f8f8f;
  }
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; }
body { background: var(--map); color: var(--ink); font: 14px/1.45 var(--ui); display: flex; }
button { font: inherit; color: inherit; }
:focus-visible { outline: 2px solid var(--blue); outline-offset: 2px; }

/* chapter list */
nav { width: 260px; flex: none; overflow: auto; background: var(--panel); border-right: 1px solid var(--line); padding: 18px 10px 14px; display: flex; flex-direction: column; }
nav h1 { font-size: 16px; font-weight: 650; margin: 0 10px 14px; letter-spacing: -.01em; }
nav .group { display: flex; align-items: center; gap: 8px; margin: 14px 10px 4px; font-size: 13px; font-weight: 600; color: var(--muted); }
.chapter { position: relative; display: flex; align-items: center; gap: 10px; width: 100%; text-align: left; border: 0; background: transparent;
  border-radius: 6px; padding: 6px 10px; cursor: pointer; }
.chapter:hover { background: color-mix(in srgb, var(--edge) 14%, transparent); }
.chapter.on { background: var(--blue-soft); font-weight: 600; }
.chapter.on::before { content: ""; position: absolute; left: -10px; top: 6px; bottom: 6px; width: 3px; border-radius: 0 3px 3px 0; background: var(--blue); }
.chapter .t { flex: 1; }
.chapter .n { font-size: 11px; font-weight: 700; color: #fff; background: var(--bad); border-radius: 8px; padding: 0 6px; }
nav .foot { margin-top: auto; padding: 18px 10px 0; display: flex; flex-direction: column; gap: 8px; }
nav .foot button { border: 1px solid var(--line); background: transparent; border-radius: 6px; padding: 5px 10px; cursor: pointer; text-align: left; }
nav .foot button:hover { border-color: var(--edge); }
.built { color: var(--muted); font-size: 12px; }

/* map: one dot per quest coordinate */
#map { flex: 1; overflow: auto; position: relative; height: 100vh; }
#title { position: sticky; left: 0; top: 0; z-index: 2; width: max-content; padding: 18px 24px 0; pointer-events: none; }
#title h2 { margin: 0; font-size: 22px; font-weight: 650; letter-spacing: -.015em; }
#title div { color: var(--muted); font-family: var(--letter); font-style: italic; font-size: 15px; }
#canvas { position: relative; background-image: radial-gradient(circle, var(--dot) 1.4px, transparent 1.6px); }
#canvas svg { position: absolute; inset: 0; overflow: visible; pointer-events: none; }
#canvas line { stroke: var(--edge); stroke-width: 2; }
#canvas line.hot { stroke: var(--blue); stroke-width: 3; }
.q { position: absolute; display: flex; align-items: center; justify-content: center; background: var(--node);
  border: 2px solid var(--edge); border-radius: 50%; cursor: pointer; transform: translate(-50%, -50%); }
.q:hover { border-color: var(--blue); }
.q.hexagon { border-radius: 30%; }
.q.gear { border-radius: 24%; border: 3px solid var(--blue); }
.q.optional { border-style: dashed; }
.q.sel { box-shadow: 0 0 0 4px color-mix(in srgb, var(--blue) 45%, transparent); }
.q .check { color: var(--blue); font-size: 18px; font-weight: 700; }
.q .label { position: absolute; top: 100%; margin-top: 5px; max-width: 124px; width: max-content; text-align: center; font-size: 11.5px; line-height: 1.25;
  color: var(--ink); background: color-mix(in srgb, var(--map) 88%, transparent); padding: 0 4px; border-radius: 3px; pointer-events: none; }
.q .badge { position: absolute; top: -7px; right: -7px; min-width: 18px; height: 18px; border-radius: 9px; padding: 0 4px;
  background: var(--warn); color: #fff; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.q .badge.bad { background: var(--bad); }
.ext { position: absolute; transform: translate(-100%, -50%); max-width: 150px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  font-size: 11.5px; padding: 1px 8px; border: 1px dashed var(--edge); border-radius: 10px; background: var(--panel); color: var(--muted); cursor: pointer; }
.ext:hover { color: var(--blue); border-color: var(--blue); }

/* item icons */
.icon { position: relative; flex: none; display: inline-block; }
.icon img { image-rendering: pixelated; object-fit: cover; object-position: top; display: block; }
.icon.flat img { width: 100%; height: 100%; }
.icon.cube img { position: absolute; left: 0; top: 0; width: 16px; height: 16px; transform-origin: 0 0; }
.icon.none { border: 1px dashed var(--edge); border-radius: 4px; font-size: 10px; color: var(--muted); display: inline-flex; align-items: center; justify-content: center; }

/* inventory slot, as in-game: dark top-left edge, light bottom-right edge, count bottom-right */
.slot { position: relative; flex: none; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: var(--slot);
  border: 2px solid; border-color: var(--slot-dark) var(--slot-light) var(--slot-light) var(--slot-dark); }
.slot .count, .slot .glyph { font-weight: 700; color: #fff; text-shadow: 2px 2px 0 #3f3f3f; }
.slot .count { position: absolute; right: 1px; bottom: -2px; font-size: 13px; }
.slot .glyph { font-size: 15px; }
.slot .glyph.xp { color: #b4f05a; font-size: 12px; }

/* popup */
#overlay { position: fixed; inset: 0; z-index: 10; background: rgb(14 20 26 / .5); display: none; align-items: center; justify-content: center; padding: 24px 16px; }
#overlay.open { display: flex; }
.dialog { background: var(--panel); border-radius: 10px; box-shadow: 0 18px 50px rgb(0 0 0 / .35); width: 700px; max-width: 100%; max-height: 100%;
  overflow: auto; display: flex; flex-direction: column; }
.dialog:focus { outline: none; }
#overlay.open .dialog { animation: open .14s ease-out; }
@keyframes open { from { opacity: 0; transform: translateY(6px) scale(.985); } }
@media (prefers-reduced-motion: reduce) { #overlay.open .dialog { animation: none; } }
.head { display: flex; gap: 14px; align-items: center; padding: 18px 22px 16px; }
.head h2 { font-size: 20px; font-weight: 650; letter-spacing: -.01em; margin: 0; }
.head .sub { color: var(--muted); font-family: var(--letter); font-style: italic; font-size: 15px; }
.head .x { margin-left: auto; align-self: flex-start; font-size: 18px; line-height: 1; border: 0; background: transparent; color: var(--muted); cursor: pointer; padding: 6px 8px; border-radius: 6px; }
.head .x:hover { background: var(--foot); color: var(--ink); }
.ref { display: flex; gap: 8px; align-items: center; margin-top: 6px; }
.ref code { font: 12.5px/1.6 ui-monospace, Consolas, monospace; background: var(--foot); border-radius: 4px; padding: 1px 7px; }
.ref button { font-size: 12px; border: 1px solid var(--line); background: transparent; border-radius: 4px; padding: 1px 8px; cursor: pointer; }
.ref button:hover { border-color: var(--edge); }
.tag { font-size: 12px; color: var(--muted); border: 1px dashed var(--edge); border-radius: 10px; padding: 0 8px; }
.letter { margin: 0 22px; padding: 18px 22px; background: var(--paper); color: var(--paper-ink); border: 1px solid var(--paper-edge); border-radius: 4px;
  font: 16px/1.65 var(--letter); white-space: pre-wrap; box-shadow: 0 1px 0 var(--paper-edge), 0 3px 0 -1px var(--paper); }
.ledger { display: grid; grid-template-columns: 1fr 1fr; gap: 18px 28px; padding: 22px 22px 22px; }
.ledger h3, .path h3 { font-size: 13px; font-weight: 650; color: var(--muted); margin: 0 0 10px; }
ul.items { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
ul.items li { display: flex; align-items: center; gap: 12px; }
ul.items .name { display: flex; flex-direction: column; line-height: 1.25; }
ul.items .id { color: var(--muted); font-size: 11.5px; }
.notes { margin: 0 22px 20px; padding: 10px 14px; border-radius: 6px; background: var(--warn-soft); }
.notes h3 { font-size: 13px; font-weight: 650; color: var(--warn); margin: 0 0 4px; }
.path { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 28px; padding: 16px 22px 20px; background: var(--foot); border-top: 1px solid var(--line); margin-top: auto; }
ul.links { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px; }
ul.links li { display: flex; align-items: center; gap: 8px; }
a.go { color: var(--blue); cursor: pointer; text-decoration: none; }
a.go:hover { text-decoration: underline; }
a.go .chap { color: var(--muted); }
.finding { padding: 3px 0; }
.finding.covered a.go { color: var(--bad); }
.empty { color: var(--muted); }
.findings-body { padding: 0 22px 22px; }

@media (max-width: 700px) {
  body { flex-direction: column; }
  nav { width: auto; max-height: 38vh; border-right: 0; border-bottom: 1px solid var(--line); }
  #map { height: auto; flex: 1; }
  .ledger, .path { grid-template-columns: 1fr; }
  .letter { margin: 0 16px; padding: 14px 16px; }
}
</style>
</head>
<body>
<nav id="chapters"><h1>Quest Explorer</h1></nav>
<div id="map"><div id="title"></div><div id="canvas"></div></div>
<div id="overlay"><div class="dialog" role="dialog" aria-modal="true" tabindex="-1" id="dialog"></div></div>
<script type="application/json" id="data">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById("data").textContent);
const UNIT = 64, PAD = 200;
const chapters = new Map(DATA.chapters.map(c => [c.slug, c]));
const quests = new Map();
for (const c of DATA.chapters) for (const q of c.quests) quests.set(c.slug + ":" + q.slug, Object.assign(q, {chapter: c.slug}));
const findingsOf = new Map();
for (const f of DATA.findings) {
  const k = f.chapter + ":" + f.slug;
  if (!findingsOf.has(k)) findingsOf.set(k, []);
  findingsOf.get(k).push(f);
}
let current = null, selected = null;

function el(tag, attrs, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === "class") e.className = v; else if (k === "text") e.textContent = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v);
  }
  for (const c of children) if (c != null) e.append(c);
  return e;
}

function icon(id, size) {
  const info = DATA.items[id];
  const box = el("span", {class: "icon " + (info ? info.kind : "none"), title: info ? info.name + "\n" + id : id});
  box.style.width = box.style.height = size + "px";
  if (!info || info.kind === "none") { box.textContent = "?"; return box; }
  if (info.kind === "flat") { box.append(el("img", {src: info.textures[0], alt: ""})); return box; }
  const k = size / 32;  // three faces of a 16px texture, mapped onto an isometric cube of the box size
  const faces = [[k, -k / 2, k, k / 2, 0, size / 4, 1], [k, k / 2, 0, k, 0, size / 4, 0.82], [k, -k / 2, 0, k, size / 2, size / 2, 0.64]];
  faces.forEach(([a, b, c, d, e, f, light], i) => {
    const img = el("img", {src: info.textures[i], alt: ""});
    img.style.transform = `matrix(${a},${b},${c},${d},${e},${f})`;
    img.style.filter = `brightness(${light})`;
    box.append(img);
  });
  return box;
}

function itemName(id) { return DATA.items[id] ? DATA.items[id].name : id; }

function slot(content, count) {
  return el("span", {class: "slot"}, content, count > 1 ? el("span", {class: "count", text: count}) : null);
}

function entry(e) {
  const row = (s, name, id) => el("li", {}, s, el("span", {class: "name"}, el("span", {text: name}), id ? el("span", {class: "id", text: id}) : null));
  if (e.type === "item") return row(slot(icon(e.item, 28), e.count || 1), itemName(e.item), e.item);
  if (e.type === "xp") return row(slot(el("span", {class: "glyph xp", text: "XP"})), e.amount + " experience");
  if (e.type === "checkmark") return row(slot(el("span", {class: "glyph", text: "✓"})), "Tick it off", "No item needed; the player confirms it in the book.");
  if (e.type === "advancement") return row(slot(el("span", {class: "glyph", text: "★"})), "Advancement", e.advancement);
  if (e.type === "observation") return row(slot(el("span", {class: "glyph", text: "👁"})), "Look at it", e.observe);
  return row(slot(el("span", {class: "glyph", text: "?"})), e.type || "Unknown", JSON.stringify(e));
}

function sidebar() {
  const nav = document.getElementById("chapters");
  for (const g of DATA.groups) {
    nav.append(el("div", {class: "group"}, icon(g.icon, 16), el("span", {text: g.title})));
    for (const c of DATA.chapters.filter(c => c.group === g.slug)) {
      const bad = DATA.findings.filter(f => f.chapter === c.slug).length;
      nav.append(el("button", {class: "chapter", "data-chapter": c.slug, onclick: () => go(c.slug, null)},
        c.icon ? icon(c.icon, 20) : null, el("span", {class: "t", text: c.title}), bad ? el("span", {class: "n", text: bad}) : null));
    }
  }
  nav.append(el("div", {class: "foot"},
    el("button", {text: DATA.findings.length ? "Show " + DATA.findings.length + " findings" : "No findings", onclick: () => findingsPopup()}),
    el("span", {class: "built", text: "Built " + DATA.built})));
}

function drawMap(slug) {
  const c = chapters.get(slug), canvas = document.getElementById("canvas");
  canvas.replaceChildren();
  const xs = c.quests.map(q => q.x), ys = c.quests.map(q => q.y);
  const minX = Math.min(...xs), minY = Math.min(...ys);
  const px = q => (q.x - minX) * UNIT + PAD, py = q => (q.y - minY) * UNIT + PAD / 2;
  canvas.style.width = (Math.max(...xs) - minX) * UNIT + PAD * 2 + "px";
  canvas.style.height = (Math.max(...ys) - minY) * UNIT + PAD * 1.5 + "px";
  canvas.style.backgroundSize = UNIT + "px " + UNIT + "px";
  canvas.style.backgroundPosition = (PAD % UNIT - UNIT / 2) + "px " + ((PAD / 2) % UNIT - UNIT / 2) + "px";
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  canvas.append(svg);
  for (const q of c.quests) {
    let ext = 0;
    for (const [dc, ds] of q.deps) {
      const d = quests.get(dc + ":" + ds);
      if (!d) continue;
      if (dc === slug) {
        const x1 = px(d), y1 = py(d), x2 = px(q), y2 = py(q), len = Math.hypot(x2 - x1, y2 - y1) || 1;
        // an arrow from below would end under the target's label, so it stops below the label
        const r1 = 22 * d.size + 2, r2 = 22 * q.size + 2 + (y1 - y2 > Math.abs(x2 - x1) ? 30 : 0);
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", x1 + (x2 - x1) * r1 / len); line.setAttribute("y1", y1 + (y2 - y1) * r1 / len);
        line.setAttribute("x2", x2 - (x2 - x1) * r2 / len); line.setAttribute("y2", y2 - (y2 - y1) * r2 / len);
        line.setAttribute("marker-end", "url(#arrow)");
        line.dataset.from = dc + ":" + ds; line.dataset.to = slug + ":" + q.slug;
        svg.append(line);
      } else {
        const m = el("span", {class: "ext", text: "← " + chapters.get(dc).title + ": " + d.title,
          title: "from " + chapters.get(dc).title + ": " + d.title + " (" + dc + ":" + ds + ")", onclick: () => go(dc, ds)});
        m.style.left = px(q) - 26 * q.size - 4 + "px";
        m.style.top = py(q) - 26 * q.size + ext * 20 + "px";
        canvas.append(m);
        ext++;
      }
    }
  }
  svg.insertAdjacentHTML("afterbegin", '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>');
  svg.style.color = getComputedStyle(document.documentElement).getPropertyValue("--edge");
  for (const q of c.quests) {
    const key = slug + ":" + q.slug, size = 44 * q.size;
    const open = () => go(slug, q.slug);
    const node = el("div", {class: "q " + q.shape + (q.optional ? " optional" : ""), "data-key": key, title: q.title, tabindex: "0", role: "button",
      onclick: open, onkeydown: e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } }},
      q.icon ? icon(q.icon, Math.round(size * 0.62)) : el("span", {class: "check", text: "✓"}), el("span", {class: "label", text: q.title}));
    node.style.left = px(q) + "px"; node.style.top = py(q) + "px";
    node.style.width = node.style.height = size + "px";
    const fs = findingsOf.get(key);
    if (fs) node.append(el("span", {class: "badge" + (fs.some(f => f.kind === "covered") ? " bad" : ""), text: fs.length,
      title: fs.map(f => f.message).join("\n")}));
    canvas.append(node);
  }
}

function copy(text, button) {
  const done = () => { button.textContent = "Copied"; setTimeout(() => button.textContent = "Copy", 1200); };
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, () => fallback());
  else fallback();
  function fallback() {
    const t = el("textarea", {}); t.value = text; document.body.append(t); t.select();
    document.execCommand("copy"); t.remove(); done();
  }
}

function findingList(list) {
  return list.length ? list.map(f => el("div", {class: "finding " + f.kind},
    el("a", {class: "go", text: f.chapter + ":" + f.slug, onclick: () => go(f.chapter, f.slug)}), el("span", {text: " " + f.message})))
    : [el("div", {class: "empty", text: "Nothing to report: no task is covered by earlier rewards, no quests share a spot."})];
}

function questLink(key) {
  const q = quests.get(key);
  const other = q && q.chapter !== current ? el("span", {class: "chap", text: chapters.get(q.chapter).title + ": "}) : null;
  return el("li", {}, q && q.icon ? icon(q.icon, 20) : el("span", {class: "icon none", text: "✓", style: "width:20px;height:20px"}),
    el("a", {class: "go", title: key, onclick: () => { const [c, s] = key.split(":"); go(c, s); }}, other, q ? q.title : key));
}

function show(...parts) {
  const dialog = document.getElementById("dialog");
  dialog.replaceChildren(...parts.filter(x => x != null));
  document.getElementById("overlay").classList.add("open");
  dialog.scrollTop = 0;
  dialog.focus({preventScroll: true});
}

function close() {
  document.getElementById("overlay").classList.remove("open");
  if (selected) {
    const key = current + ":" + selected;
    go(current, null);
    const n = document.querySelector(`.q[data-key="${key}"]`);
    if (n) n.focus({preventScroll: true});
  }
}

function head(iconId, title, ...below) {
  return el("div", {class: "head"}, iconId ? slot(icon(iconId, 28)) : null,
    el("div", {}, el("h2", {text: title}), ...below),
    el("button", {class: "x", title: "Close (Esc)", "aria-label": "Close", text: "✕", onclick: close}));
}

function findingsPopup() {
  show(head(null, "Findings", el("div", {class: "sub", text: DATA.findings.length + " in the whole quest line"})),
    el("div", {class: "findings-body"}, ...findingList(DATA.findings)));
}

function popup() {
  const key = current + ":" + selected, q = quests.get(key);
  const button = el("button", {text: "Copy", onclick: () => copy(key, button)});
  const unlocks = [...quests.values()].filter(o => o.deps.some(([dc, ds]) => dc + ":" + ds === key)).map(o => o.chapter + ":" + o.slug);
  const fs = findingsOf.get(key) || [];
  const items = (list, none) => list.length ? el("ul", {class: "items"}, ...list.map(entry)) : el("div", {class: "empty", text: none});
  const links = (list, none) => list.length ? el("ul", {class: "links"}, ...list.map(questLink)) : el("div", {class: "empty", text: none});
  show(
    head(q.icon, q.title, q.subtitle ? el("div", {class: "sub", text: q.subtitle}) : null,
      el("div", {class: "ref"}, el("code", {text: key}), button, q.optional ? el("span", {class: "tag", text: "Optional"}) : null)),
    q.description ? el("div", {class: "letter", text: q.description}) : null,
    el("div", {class: "ledger"},
      el("section", {}, el("h3", {text: "Tasks"}), items(q.tasks, "No tasks.")),
      el("section", {}, el("h3", {text: "Rewards"}), items(q.rewards, "No rewards."))),
    fs.length ? el("div", {class: "notes"}, el("h3", {text: "Findings"}), ...findingList(fs)) : null,
    el("div", {class: "path"},
      el("section", {}, el("h3", {text: "Comes after"}), links(q.deps.map(d => d.join(":")), "Nothing; this quest is open from the start.")),
      el("section", {}, el("h3", {text: "Leads to"}), links(unlocks, "Nothing; this is the end of its line."))));
}

function go(chapter, slug, fromHash) {
  if (!chapters.has(chapter)) return;
  if (chapter !== current) {
    current = chapter;
    drawMap(chapter);
    const c = chapters.get(chapter);
    document.getElementById("title").replaceChildren(el("h2", {text: c.title}), c.subtitle ? el("div", {text: c.subtitle}) : el("div"));
  }
  selected = slug && quests.has(chapter + ":" + slug) ? slug : null;
  document.querySelectorAll(".chapter").forEach(t => t.classList.toggle("on", t.dataset.chapter === current));
  document.querySelectorAll(".q").forEach(n => n.classList.toggle("sel", n.dataset.key === current + ":" + selected));
  document.querySelectorAll("#canvas line").forEach(l => l.classList.toggle("hot", !!selected && (l.dataset.to === current + ":" + selected || l.dataset.from === current + ":" + selected)));
  if (selected) popup(); else document.getElementById("overlay").classList.remove("open");
  if (selected) {
    const n = document.querySelector(`.q[data-key="${current}:${selected}"]`);
    if (n) n.scrollIntoView({block: "nearest", inline: "nearest"});
  }
  if (!fromHash) history.replaceState(null, "", "#" + current + (selected ? ":" + selected : ""));
}

function fromHash() {
  const [c, s] = decodeURIComponent(location.hash.slice(1)).split(":");
  if (chapters.has(c)) go(c, s, true); else go(DATA.chapters[0].slug, null);
}

sidebar();
fromHash();
window.addEventListener("hashchange", fromHash);
document.getElementById("overlay").addEventListener("click", e => { if (e.target.id === "overlay") close(); });
document.addEventListener("keydown", e => { if (e.key === "Escape" && document.getElementById("overlay").classList.contains("open")) close(); });
</script>
</body>
</html>
"""
